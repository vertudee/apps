use axum::{
    extract::{Form, Json, Path, Query, State},
    http::{header, HeaderMap, StatusCode},
    response::{Html, IntoResponse, Redirect},
    routing::{get, post},
    Router,
};
use base64::{engine::general_purpose, Engine};
use chrono::{Duration, Utc};
use http::HeaderValue;
use jsonwebtoken::{encode, Algorithm, DecodingKey, EncodingKey, Header};
use jsonwebtoken::{
    jwk::{CommonParameters, Jwk},
    Validation,
};
use once_cell::sync::Lazy;
use rsa::pkcs8::{DecodePublicKey, EncodePrivateKey, EncodePublicKey};
use rsa::traits::PublicKeyParts;
use rsa::RsaPrivateKey;
use serde::{Deserialize, Serialize};
use serde_json::json;
use sha2::Digest;
use std::{
    collections::{HashMap, HashSet},
    net::SocketAddr,
    sync::{Arc, RwLock},
};
use tokio::{net::TcpListener, task::JoinHandle};
use tower_http::cors::{AllowHeaders, AllowMethods, AllowOrigin, CorsLayer};
use uuid::Uuid;

pub const KID: &str = "oauth-by-rustmcp";

// src/config.rs
use serde_json::Value;

#[derive(Debug, Clone)]
pub struct IssuerConfig {
    pub scheme: String,
    pub host: String,
    pub port: u16,

    // OIDC / OAuth capabilities
    pub scopes_supported: HashSet<String>,
    pub claims_supported: Vec<String>,
    pub grant_types_supported: HashSet<String>,
    pub response_types_supported: HashSet<String>,
    pub token_endpoint_auth_methods_supported: HashSet<String>,
    pub code_challenge_methods_supported: HashSet<String>,
    pub subject_types_supported: Vec<String>,
    pub id_token_signing_alg_values_supported: Vec<String>,
    pub generate_client_secret_for_dcr: bool,
    pub allowed_origins: Vec<String>,
}

impl Default for IssuerConfig {
    fn default() -> Self {
        let mut scopes = HashSet::new();
        scopes.extend([
            "openid".into(),
            "profile".into(),
            "email".into(),
            "offline_access".into(),
            "address".into(),
            "phone".into(),
        ]);

        let mut grants = HashSet::new();
        grants.extend([
            "authorization_code".into(),
            "refresh_token".into(),
            "client_credentials".into(),
        ]);

        let mut auth_methods = HashSet::new();
        auth_methods.extend([
            "client_secret_basic".into(),
            "client_secret_post".into(),
            "none".into(),
            "private_key_jwt".into(),
        ]);

        Self {
            scheme: "http".into(),
            host: "localhost".into(),
            port: 0, // random
            scopes_supported: scopes,
            claims_supported: vec![
                "sub".into(),
                "name".into(),
                "given_name".into(),
                "family_name".into(),
                "email".into(),
                "email_verified".into(),
                "picture".into(),
                "locale".into(),
            ],
            generate_client_secret_for_dcr: true,
            grant_types_supported: grants,
            response_types_supported: ["code".into(), "token".into(), "id_token".into()].into(),
            token_endpoint_auth_methods_supported: auth_methods,
            code_challenge_methods_supported: ["plain".into(), "S256".into()].into(),
            subject_types_supported: vec!["public".into()],
            id_token_signing_alg_values_supported: vec!["RS256".into()],
            allowed_origins: vec![
                "http://localhost:3001".to_string(),
                "http://localhost:8080".to_string(),
                "http://localhost:6274".to_string(),
            ],
        }
    }
}

impl IssuerConfig {
    pub fn to_discovery_document(&self, issuer: String) -> Value {
        let iss = issuer;
        json!({
            "issuer": iss,
            "authorization_endpoint": format!("{}/authorize", iss),
            "token_endpoint": format!("{}/token", iss),
            "userinfo_endpoint": format!("{}/userinfo", iss),
            "jwks_uri": format!("{}/.well-known/jwks.json", iss),
            "registration_endpoint": format!("{}/register", iss),
            "revocation_endpoint": format!("{}/revoke", iss),
            "introspection_endpoint": format!("{}/introspect", iss),
            "scopes_supported": self.scopes_supported.iter().collect::<Vec<_>>(),
            "claims_supported": &self.claims_supported,
            "grant_types_supported": self.grant_types_supported.iter().collect::<Vec<_>>(),
            "response_types_supported": self.response_types_supported.iter().collect::<Vec<_>>(),
            "token_endpoint_auth_methods_supported": self.token_endpoint_auth_methods_supported.iter().collect::<Vec<_>>(),
            "code_challenge_methods_supported": self.code_challenge_methods_supported.iter().collect::<Vec<_>>(),
            "subject_types_supported": &self.subject_types_supported,
            "id_token_signing_alg_values_supported": &self.id_token_signing_alg_values_supported,
        })
    }

    pub fn validate_scope(&self, scope: &str) -> Result<String, String> {
        let requested: HashSet<_> = scope.split_whitespace().map(|s| s.to_string()).collect();
        let unknown: Vec<_> = requested
            .difference(&self.scopes_supported)
            .cloned()
            .collect();
        if unknown.is_empty() {
            Ok(scope.to_string())
        } else {
            Err(format!("invalid_scope: {}", unknown.join(" ")))
        }
    }

    pub fn validate_grant_type(&self, grant: &str) -> bool {
        self.grant_types_supported.contains(grant)
    }
}

// #[derive(Clone, Debug)]
// pub struct Config {
//     pub scheme: String,
//     pub host: String,
//     pub port: u16,
//     pub generate_client_secret_for_dcr: bool,
//     pub allowed_origins: Vec<String>,
// }

// impl Default for Config {
//     fn default() -> Self {
//         Self {
//             scheme: "http".to_string(),
//             host: "localhost".to_string(),
//             port: 8090,
//             generate_client_secret_for_dcr: true,
//             allowed_origins: vec![
//                 "http://localhost:3001".to_string(),
//                 "http://localhost:8080".to_string(),
//                 "http://localhost:6274".to_string(),
//             ],
//         }
//     }
// }

#[derive(Clone)]
pub struct AppState {
    pub config: Arc<IssuerConfig>,
    pub base_url: String,
    pub clients: Arc<RwLock<HashMap<String, Client>>>,
    pub codes: Arc<RwLock<HashMap<String, AuthorizationCode>>>,
    pub tokens: Arc<RwLock<HashMap<String, Token>>>,
    pub refresh_tokens: Arc<RwLock<HashMap<String, Token>>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Client {
    pub client_id: String,
    pub client_secret: Option<String>,
    pub redirect_uris: Vec<String>,
    pub grant_types: Vec<String>,
    pub response_types: Vec<String>,
    pub scope: String,
    pub token_endpoint_auth_method: String,
    pub client_name: Option<String>,
    pub client_uri: Option<String>,
    pub logo_uri: Option<String>,
    pub contacts: Vec<String>,
    pub policy_uri: Option<String>,
    pub tos_uri: Option<String>,
    pub jwks: Option<serde_json::Value>,
    pub jwks_uri: Option<String>,
    pub software_id: Option<String>,
    pub software_version: Option<String>,
    pub registration_access_token: Option<String>,
    pub registration_client_uri: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuthorizationCode {
    pub code: String,
    pub client_id: String,
    pub redirect_uri: String,
    pub scope: String,
    pub expires_at: chrono::DateTime<Utc>,
    pub code_challenge: Option<String>,
    pub code_challenge_method: Option<String>,
    pub user_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Token {
    pub access_token: String,
    pub refresh_token: Option<String>,
    pub client_id: String,
    pub scope: String,
    pub expires_at: chrono::DateTime<Utc>,
    pub user_id: String,
    pub revoked: bool,
}

impl AppState {
    pub fn new(config: IssuerConfig) -> Self {
        let base_url = format!("{}://{}:{}", config.scheme, config.host, config.port);
        Self {
            config: Arc::new(config),
            clients: Arc::new(RwLock::new(HashMap::new())),
            codes: Arc::new(RwLock::new(HashMap::new())),
            tokens: Arc::new(RwLock::new(HashMap::new())),
            refresh_tokens: Arc::new(RwLock::new(HashMap::new())),
            base_url,
        }
    }

    pub fn issuer(&self) -> &str {
        self.base_url.as_str()
    }

    pub fn register_client(
        &self,
        metadata: serde_json::Value,
    ) -> Result<Client, (StatusCode, Json<serde_json::Value>)> {
        let requested_scope = metadata
            .get("scope")
            .and_then(|v| v.as_str())
            .unwrap_or("openid");

        self.config
            .validate_scope(requested_scope)
            .map_err(|err| (StatusCode::BAD_REQUEST, Json(json!({"error": err}))))?;

        let client_id = Uuid::new_v4().to_string();

        let client_secret = if self.config.generate_client_secret_for_dcr
            || metadata
                .get("token_endpoint_auth_method")
                .and_then(|v| v.as_str())
                != Some("none")
        {
            Some(generate_token())
        } else {
            None
        };

        let redirect_uris = metadata
            .get("redirect_uris")
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|u| u.as_str().map(|s| s.to_string()))
                    .collect::<Vec<String>>()
            })
            .unwrap_or_default();

        if redirect_uris.is_empty()
            && metadata.get("grant_types").map(|v| {
                v.as_array()
                    .map(|a| a.contains(&json!("client_credentials")))
            }) != Some(Some(true))
        {
            return Err((
                StatusCode::BAD_REQUEST,
                Json(json!({"error": "redirect_uris required"})),
            ));
        }

        let client = Client {
            client_id: client_id.clone(),
            client_secret: client_secret.clone(),
            redirect_uris,
            grant_types: metadata
                .get("grant_types")
                .and_then(|v| v.as_array())
                .map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(|s| s.to_string()))
                        .collect()
                })
                .unwrap_or_else(|| vec!["authorization_code".to_string()]),
            response_types: metadata
                .get("response_types")
                .and_then(|v| v.as_array())
                .map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(|s| s.to_string()))
                        .collect()
                })
                .unwrap_or_else(|| vec!["code".to_string()]),
            scope: metadata
                .get("scope")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            token_endpoint_auth_method: metadata
                .get("token_endpoint_auth_method")
                .and_then(|v| v.as_str())
                .unwrap_or("client_secret_basic")
                .to_string(),
            client_name: metadata
                .get("client_name")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            client_uri: metadata
                .get("client_uri")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            logo_uri: metadata
                .get("logo_uri")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            contacts: metadata
                .get("contacts")
                .and_then(|v| v.as_array())
                .map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(|s| s.to_string()))
                        .collect()
                })
                .unwrap_or_default(),
            policy_uri: metadata
                .get("policy_uri")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            tos_uri: metadata
                .get("tos_uri")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            jwks: metadata.get("jwks").cloned(),
            jwks_uri: metadata
                .get("jwks_uri")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            software_id: metadata
                .get("software_id")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            software_version: metadata
                .get("software_version")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            registration_access_token: None,
            registration_client_uri: Some(format!("{}/register/{}", self.issuer(), client_id)),
        };

        self.clients
            .write()
            .unwrap()
            .insert(client_id.clone(), client.clone());

        Ok(client)
    }

    pub fn generate_token(
        &self,
        client: &Client,
        options: crate::testkit::JwtOptions,
    ) -> Result<Token, jsonwebtoken::errors::Error> {
        let user_id = options.user_id.clone();
        let jwt = self.generate_jwt(client, options)?;
        let refresh_token = generate_token();
        let token = Token {
            access_token: jwt.clone(),
            refresh_token: Some(refresh_token),
            client_id: client.client_id.clone(),
            scope: client.scope.clone(),
            expires_at: Utc::now() + Duration::hours(1),
            user_id,
            revoked: false,
        };

        self.tokens
            .write()
            .unwrap()
            .insert(jwt.clone(), token.clone());
        Ok(token)
    }
    pub fn generate_jwt(
        &self,
        client: &Client,
        options: crate::testkit::JwtOptions,
    ) -> Result<String, jsonwebtoken::errors::Error> {
        let scope = options.scope.unwrap_or_else(|| client.scope.clone());
        issue_jwt(
            self.issuer(),
            &client.client_id,
            &options.user_id,
            &scope,
            options.expires_in,
        )
    }

    pub fn router(self) -> Router {
        let cors = build_cors_layer(&self.config);
        Router::new()
            .route(
                "/.well-known/openid-configuration",
                get(well_known_openid_configuration),
            )
            .route("/.well-known/jwks.json", get(jwks))
            .route("/register", post(register_client))
            .route("/register/{client_id}", get(get_client))
            .route("/authorize", get(authorize))
            .route("/token", post(token_endpoint))
            .route("/introspect", post(introspect))
            .route("/revoke", post(revoke))
            .route("/userinfo", get(userinfo))
            .route("/error", get(error_page))
            .with_state(self)
            .layer(cors)
    }

    pub async fn start(mut self) -> (SocketAddr, JoinHandle<()>) {
        let port = self.config.port;
        let addr = SocketAddr::from(([127, 0, 0, 1], port));
        let listener = TcpListener::bind(addr).await.unwrap();
        let local_addr = listener.local_addr().unwrap();
        let base_url = format!(
            "{}://{}:{}",
            self.config.scheme,
            self.config.host,
            local_addr.port()
        );
        self.base_url = base_url;

        let router = self.router();
        let handle = tokio::spawn(async move {
            axum::serve(listener, router).await.unwrap();
        });
        (local_addr, handle)
    }
}

fn generate_code() -> String {
    Uuid::new_v4().to_string()[..20].to_string()
}

fn generate_token() -> String {
    format!("tok_{}", Uuid::new_v4().to_string().replace("-", ""))
}

fn issue_jwt(
    issuer: &str,
    client_id: &str,
    user_id: &str,
    requested_scope: &str,
    expires_in: i64,
) -> Result<String, jsonwebtoken::errors::Error> {
    let iat = Utc::now().timestamp() as usize;
    let exp = (Utc::now() + Duration::seconds(expires_in)).timestamp() as usize;

    // Filter and clean up requested scopes
    let scopes: Vec<&str> = requested_scope.split_whitespace().collect();

    // Construct the JWT claims (payload)
    let claims = Claims {
        iss: issuer.to_string(),
        sub: user_id.to_string(),
        aud: client_id.to_string(),
        exp,
        iat,
        scope: Some(scopes.join(" ")), // Only requested scopes
        auth_time: Some(iat),
        // New claims
        typ: "Bearer".to_string(), // This is part of the payload
        azp: Some(client_id.to_string()),
        sid: Some(format!("sid-{}", Uuid::new_v4())),
        jti: Uuid::new_v4().to_string(),
    };

    // Build the JWT header with typ: JWT
    let mut header = Header::new(Algorithm::RS256);
    header.typ = Some("JWT".to_string());
    header.kid = Some(KID.to_string());

    // Encode (sign) the token
    encode(&header, &claims, &KEYS.encoding)
}

// === Global RSA Key (for JWT signing) ===
pub static KEYS: Lazy<Keys> = Lazy::new(|| {
    let mut rng = rand::thread_rng();
    let private_key = RsaPrivateKey::new(&mut rng, 2048).expect("failed to generate key");
    let public_key = private_key.to_public_key();

    // Generate PEMs
    let private_pem = private_key
        .to_pkcs8_pem(rsa::pkcs8::LineEnding::LF)
        .expect("failed to encode private key")
        .to_string();

    let public_pem = public_key
        .to_public_key_pem(rsa::pkcs8::LineEnding::LF)
        .expect("failed to encode public key")
        .to_string();

    let encoding_key = EncodingKey::from_rsa_pem(private_pem.as_bytes()).unwrap();
    let decoding_key = DecodingKey::from_rsa_pem(public_pem.as_bytes()).unwrap();

    Keys {
        encoding: encoding_key,
        decoding: decoding_key,
        public_pem, // Store it
    }
});

static JWKS_JSON: Lazy<serde_json::Value> = Lazy::new(|| {
    let public_key = rsa::RsaPublicKey::from_public_key_pem(&KEYS.public_pem)
        .expect("Failed to parse stored public key");

    let jwk = Jwk {
        common: CommonParameters {
            key_algorithm: Some(jsonwebtoken::jwk::KeyAlgorithm::RS256),
            key_id: Some(KID.to_string()),
            ..Default::default()
        },
        algorithm: jsonwebtoken::jwk::AlgorithmParameters::RSA(
            jsonwebtoken::jwk::RSAKeyParameters {
                n: general_purpose::URL_SAFE_NO_PAD.encode(public_key.n().to_bytes_be()),
                e: general_purpose::URL_SAFE_NO_PAD.encode(public_key.e().to_bytes_be()),
                key_type: jsonwebtoken::jwk::RSAKeyType::RSA,
            },
        ),
    };

    json!({ "keys": [jwk] })
});

#[allow(unused)]
pub struct Keys {
    pub encoding: EncodingKey,
    pub decoding: DecodingKey,
    pub public_pem: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct AccessToken {
    access_token: String,
    token_type: String,
    expires_in: i64,
    scope: Option<String>,
    refresh_token: Option<String>,
    id_token: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Claims {
    iss: String,
    sub: String,
    aud: String,
    exp: usize,
    iat: usize,
    scope: Option<String>,
    auth_time: Option<usize>,
    typ: String,         // Token type, e.g., "Bearer"
    azp: Option<String>, // Authorized party (client_id)
    sid: Option<String>, // Session ID
    jti: String,         // Unique token ID
}

// 'oauth-authorization-server' | 'oauth-protected-resource' | 'openid-configuration',
async fn well_known_openid_configuration(State(state): State<AppState>) -> impl IntoResponse {
    let discovery = state.config.to_discovery_document(state.base_url);
    (StatusCode::OK, Json(discovery))
}

async fn jwks() -> impl IntoResponse {
    (StatusCode::OK, Json(JWKS_JSON.clone()))
}

async fn register_client(
    State(state): State<AppState>,
    Json(metadata): Json<serde_json::Value>,
) -> impl IntoResponse {
    let requested_scope = metadata
        .get("scope")
        .and_then(|v| v.as_str())
        .unwrap_or("openid");

    match state.config.validate_scope(requested_scope) {
        Ok(_) => { /* continue */ }
        Err(e) => {
            return (
                StatusCode::BAD_REQUEST,
                Json(json!({ "error": "invalid_scope", "error_description": e })),
            );
        }
    };

    let client_id = Uuid::new_v4().to_string();

    let client_secret = if state.config.generate_client_secret_for_dcr
        || metadata
            .get("token_endpoint_auth_method")
            .and_then(|v| v.as_str())
            != Some("none")
    {
        Some(generate_token())
    } else {
        None
    };

    let redirect_uris = metadata
        .get("redirect_uris")
        .and_then(|v| v.as_array())
        .map(|arr| {
            arr.iter()
                .filter_map(|u| u.as_str().map(|s| s.to_string()))
                .collect::<Vec<String>>()
        })
        .unwrap_or_default();

    if redirect_uris.is_empty()
        && metadata.get("grant_types").map(|v| {
            v.as_array()
                .map(|a| a.contains(&json!("client_credentials")))
        }) != Some(Some(true))
    {
        return (
            StatusCode::BAD_REQUEST,
            Json(json!({"error": "redirect_uris required"})),
        );
    }

    let client = Client {
        client_id: client_id.clone(),
        client_secret: client_secret.clone(),
        redirect_uris,
        grant_types: metadata
            .get("grant_types")
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str().map(|s| s.to_string()))
                    .collect()
            })
            .unwrap_or_else(|| vec!["authorization_code".to_string()]),
        response_types: metadata
            .get("response_types")
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str().map(|s| s.to_string()))
                    .collect()
            })
            .unwrap_or_else(|| vec!["code".to_string()]),
        scope: metadata
            .get("scope")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string(),
        token_endpoint_auth_method: metadata
            .get("token_endpoint_auth_method")
            .and_then(|v| v.as_str())
            .unwrap_or("client_secret_basic")
            .to_string(),
        client_name: metadata
            .get("client_name")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        client_uri: metadata
            .get("client_uri")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        logo_uri: metadata
            .get("logo_uri")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        contacts: metadata
            .get("contacts")
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str().map(|s| s.to_string()))
                    .collect()
            })
            .unwrap_or_default(),
        policy_uri: metadata
            .get("policy_uri")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        tos_uri: metadata
            .get("tos_uri")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        jwks: metadata.get("jwks").cloned(),
        jwks_uri: metadata
            .get("jwks_uri")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        software_id: metadata
            .get("software_id")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        software_version: metadata
            .get("software_version")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string()),
        registration_access_token: None,
        registration_client_uri: Some(format!("{}/register/{}", state.issuer(), client_id)),
    };

    state
        .clients
        .write()
        .unwrap()
        .insert(client_id.clone(), client.clone());

    let response = json!({
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "client_id_issued_at": Utc::now().timestamp(),
        "registration_client_uri": client.registration_client_uri,
        "registration_access_token": Uuid::new_v4().to_string(),
        "redirect_uris": client.redirect_uris,
        "grant_types": client.grant_types,
        "response_types": client.response_types,
        "scope": client.scope,
        "token_endpoint_auth_method": client.token_endpoint_auth_method
    });

    (StatusCode::CREATED, Json(response))
}

async fn get_client(
    State(state): State<AppState>,
    Path(client_id): Path<String>,
) -> impl IntoResponse {
    if let Some(client) = state.clients.read().unwrap().get(&client_id) {
        let response = json!({
            "client_id": client.client_id,
            "client_name": client.client_name,
            "redirect_uris": client.redirect_uris,
            "grant_types": client.grant_types,
            "scope": client.scope
        });
        (StatusCode::OK, Json(response))
    } else {
        (
            StatusCode::NOT_FOUND,
            Json(json!({"error": "client not found"})),
        )
    }
}

#[derive(Deserialize)]
struct AuthorizeQuery {
    response_type: String,
    client_id: String,
    redirect_uri: Option<String>,
    scope: Option<String>,
    state: Option<String>,
    code_challenge: Option<String>,
    code_challenge_method: Option<String>,
}

async fn authorize(
    State(state): State<AppState>,
    Query(params): Query<AuthorizeQuery>,
) -> impl IntoResponse {
    let clients = state.clients.read().unwrap();
    let client = match clients.get(&params.client_id) {
        Some(c) => c,
        None => {
            return Redirect::to(&format!(
                "/error?error=invalid_client&state={}",
                params.state.as_deref().unwrap_or("")
            ))
            .into_response();
        }
    };

    if params.response_type != "code" {
        return Redirect::to(&format!(
            "/error?error=unsupported_response_type&state={}",
            params.state.as_deref().unwrap_or("")
        ))
        .into_response();
    }

    let redirect_uri = match &params.redirect_uri {
        Some(uri) => {
            if !client.redirect_uris.contains(uri) {
                return Redirect::to(&format!(
                    "/error?error=invalid_request&state={}",
                    params.state.as_deref().unwrap_or("")
                ))
                .into_response();
            }
            uri.clone()
        }
        None => client.redirect_uris.first().unwrap().clone(),
    };

    let code = generate_code();

    // Compute the allowed scope: intersection of requested and registered
    let requested_scopes: HashSet<String> = params
        .scope
        .clone()
        .unwrap_or_default()
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();

    let registered_scopes: HashSet<String> = client
        .scope
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();

    let granted_scopes: Vec<String> = requested_scopes
        .intersection(&registered_scopes)
        .cloned()
        .collect();

    let final_scope = granted_scopes.join(" ");

    let auth_code = AuthorizationCode {
        code: code.clone(),
        client_id: params.client_id.clone(),
        redirect_uri: redirect_uri.clone(),
        scope: final_scope, // use filtered scopes
        expires_at: Utc::now() + Duration::minutes(10),
        code_challenge: params.code_challenge.clone(),
        code_challenge_method: params.code_challenge_method.clone(),
        user_id: "test-user-123".to_string(),
    };

    state.codes.write().unwrap().insert(code.clone(), auth_code);

    let redirect_url = format!(
        "{}?code={}&state={}",
        redirect_uri,
        code,
        params.state.as_deref().unwrap_or("")
    );

    Redirect::to(&redirect_url).into_response()
}

#[derive(Deserialize)]
struct TokenRequest {
    grant_type: String,
    code: Option<String>,
    _redirect_uri: Option<String>,
    client_id: Option<String>,
    _client_secret: Option<String>,
    refresh_token: Option<String>,
    code_verifier: Option<String>,
    scope: Option<String>,
}

async fn token_endpoint(
    State(state): State<AppState>,
    _headers: HeaderMap,
    Form(form): Form<TokenRequest>,
) -> impl IntoResponse {
    if form.grant_type == "authorization_code" {
        let code = form.code.as_deref().unwrap_or("");
        let code_obj = match state.codes.write().unwrap().remove(code) {
            Some(c) => c,
            None => {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({"error": "invalid_grant"})),
                )
                    .into_response();
            }
        };

        if code_obj.expires_at < Utc::now() {
            return (
                StatusCode::BAD_REQUEST,
                Json(json!({"error": "invalid_grant"})),
            )
                .into_response();
        }

        if let (Some(challenge), Some(verifier)) = (&code_obj.code_challenge, &form.code_verifier) {
            let method = code_obj.code_challenge_method.as_deref().unwrap_or("plain");
            let computed = if method == "S256" {
                general_purpose::URL_SAFE_NO_PAD.encode(sha2::Sha256::digest(verifier.as_bytes()))
            } else {
                verifier.clone()
            };
            if computed != *challenge {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({"error": "invalid_grant"})),
                )
                    .into_response();
            }
        }

        // let access_token = generate_token();
        let refresh_token = generate_token();

        let jwt = issue_jwt(
            state.issuer(),
            &code_obj.client_id,
            &code_obj.user_id,
            &code_obj.scope,
            3600,
        )
        .unwrap();

        let token = Token {
            access_token: jwt.clone(),
            refresh_token: Some(refresh_token.clone()),
            client_id: code_obj.client_id.clone(),
            scope: code_obj.scope.clone(),
            expires_at: Utc::now() + Duration::hours(1),
            user_id: code_obj.user_id.clone(),
            revoked: false,
        };

        state
            .tokens
            .write()
            .unwrap()
            .insert(jwt.clone(), token.clone());
        state
            .refresh_tokens
            .write()
            .unwrap()
            .insert(refresh_token.clone(), token);

        let response = json!({
            "access_token": jwt,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token,
            "scope": code_obj.scope
        });

        (StatusCode::OK, Json(response)).into_response()
    } else if form.grant_type == "refresh_token" {
        let rt = form.refresh_token.as_deref().unwrap_or("");
        let mut guard = state.refresh_tokens.write().unwrap();
        let token = match guard.get_mut(rt) {
            Some(t) => t,
            None => {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({"error": "invalid_grant"})),
                )
                    .into_response();
            }
        };

        if token.revoked {
            return (
                StatusCode::BAD_REQUEST,
                Json(json!({"error": "invalid_grant"})),
            )
                .into_response();
        }

        let new_access_token = issue_jwt(
            state.issuer(),
            &token.client_id,
            &token.user_id,
            &token.scope,
            3600,
        )
        .unwrap();
        let new_refresh_token = generate_token();

        let new_token = Token {
            access_token: new_access_token.clone(),
            refresh_token: Some(new_refresh_token.clone()),
            client_id: token.client_id.clone(),
            scope: token.scope.clone(),
            expires_at: Utc::now() + Duration::hours(1),
            user_id: token.user_id.clone(),
            revoked: false,
        };

        state
            .tokens
            .write()
            .unwrap()
            .insert(new_access_token.clone(), new_token.clone());
        state
            .refresh_tokens
            .write()
            .unwrap()
            .insert(new_refresh_token.clone(), new_token);

        token.revoked = true;

        let response = json!({
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": new_refresh_token,
            "scope": token.scope
        });

        (StatusCode::OK, Json(response)).into_response()
    } else if form.grant_type == "client_credentials" {
        let client_id = form.client_id.as_deref().unwrap_or("");
        let clients = state.clients.read().unwrap();
        let client = match clients.get(client_id) {
            Some(c) => c,
            None => {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({"error": "invalid_client"})),
                )
                    .into_response();
            }
        };

        // Requested scopes from request
        let requested_scopes: HashSet<String> = form
            .scope
            .as_deref()
            .unwrap_or("")
            .split_whitespace()
            .map(|s| s.to_string())
            .collect();

        if let Some(requested_scope) = form.scope.as_deref() {
            // 1. Must be supported by the issuer
            if let Err(e) = state.config.validate_scope(requested_scope) {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({
                        "error": "invalid_scope",
                        "error_description": e
                    })),
                )
                    .into_response();
            }

            // 2. Must be allowed for this client
            let client_scopes: HashSet<_> = client.scope.split_whitespace().collect();
            let requested_scopes: HashSet<_> = requested_scope.split_whitespace().collect();

            let not_permitted: Vec<_> = requested_scopes
                .difference(&client_scopes)
                .cloned()
                .collect();
            if !not_permitted.is_empty() {
                return (StatusCode::BAD_REQUEST, Json(json!({
                        "error": "invalid_scope",
                        "error_description": format!("Client not authorized for scopes: {}", not_permitted.join(" "))
                    }))).into_response();
            }
        }

        // Allowed scopes from registration
        let registered_scopes: HashSet<String> = client
            .scope
            .split_whitespace()
            .map(|s| s.to_string())
            .collect();

        // Intersection (only allowed scopes)
        let granted_scopes: Vec<String> = requested_scopes
            .intersection(&registered_scopes)
            .cloned()
            .collect();

        // If none of the requested scopes are allowed, return an error
        if granted_scopes.is_empty() && !requested_scopes.is_empty() {
            return (
                StatusCode::BAD_REQUEST,
                Json(json!({
                    "error": "invalid_scope",
                    "error_description": "Requested scopes not allowed for this client"
                })),
            )
                .into_response();
        }

        // Final scope string
        let final_scope = if requested_scopes.is_empty() {
            // No scope was requested, issue default from registration
            client.scope.clone()
        } else {
            granted_scopes.join(" ")
        };

        // Issue JWT with only granted scopes
        let access_token =
            issue_jwt(state.issuer(), client_id, "client", &final_scope, 3600).unwrap();

        let response = json!({
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": final_scope
        });

        (StatusCode::OK, Json(response)).into_response()
    } else {
        (
            StatusCode::BAD_REQUEST,
            Json(json!({"error": "unsupported_grant_type"})),
        )
            .into_response()
    }
}

async fn introspect(
    State(state): State<AppState>,
    Form(form): Form<HashMap<String, String>>,
) -> impl IntoResponse {
    let token = match form.get("token") {
        Some(t) => t,
        None => {
            return (
                StatusCode::BAD_REQUEST,
                Json(json!({"error": "invalid_request"})),
            )
                .into_response()
        }
    };

    // First check if token exists in our storage (optional but recommended)
    let stored_token = state.tokens.read().unwrap().get(token).cloned();

    // Decode the JWT (without full validation if you want to allow expired tokens for introspection)
    let mut validation = Validation::new(Algorithm::RS256);
    validation.validate_exp = false; // Allow introspection of expired tokens
    validation.required_spec_claims.clear(); // Be permissive
    validation.validate_aud = false;

    match jsonwebtoken::decode::<Claims>(token, &KEYS.decoding, &validation) {
        Ok(token_data) => {
            let claims = token_data.claims;

            // Determine if active based on your internal state + expiry
            let is_expired = Utc::now().timestamp() > claims.exp as i64;
            let is_revoked = stored_token.map(|t| t.revoked).unwrap_or(false);
            let active = !is_revoked && !is_expired;

            let mut response = json!({
                "active": active,
                "scope": claims.scope,
                "client_id": claims.aud,
                "sub": claims.sub,
                "iss": claims.iss,
                "aud": claims.aud,
                "iat": claims.iat,
                "exp": claims.exp,
                "jti": claims.jti,
                "token_type": "Bearer",
                "azp": claims.azp,
                "auth_time": claims.auth_time,
                "sid": claims.sid,
            });

            // Only include scope if present
            if claims.scope.is_none() {
                response.as_object_mut().unwrap().remove("scope");
            }

            (StatusCode::OK, Json(response)).into_response()
        }
        Err(err) => {
            println!(">>> err {:?} ", err);

            // If we can't decode it at all, it's invalid
            (StatusCode::OK, Json(json!({"active": false}))).into_response()
        }
    }
}

async fn revoke(
    State(state): State<AppState>,
    Form(form): Form<HashMap<String, String>>,
) -> impl IntoResponse {
    let token = form.get("token").cloned().unwrap_or_default();
    if let Some(t) = state.tokens.write().unwrap().get_mut(&token) {
        t.revoked = true;
    }
    if let Some(t) = state.refresh_tokens.write().unwrap().get_mut(&token) {
        t.revoked = true;
    }
    (StatusCode::OK, Json(json!({}))).into_response()
}

async fn userinfo(headers: HeaderMap, State(state): State<AppState>) -> impl IntoResponse {
    let auth = headers.get("Authorization").and_then(|v| v.to_str().ok());
    if let Some(auth) = auth {
        if let Some(token) = auth.strip_prefix("Bearer ") {
            if let Some(t) = state.tokens.read().unwrap().get(token) {
                if t.revoked || t.expires_at < Utc::now() {
                    return (
                        StatusCode::UNAUTHORIZED,
                        Json(json!({"error": "invalid_token"})),
                    )
                        .into_response();
                }
                let response = json!({
                    "sub": t.user_id,
                    "name": "Test User",
                    "email": "test@example.com",
                    "picture": "https://example.com/avatar.jpg"
                });
                return (StatusCode::OK, Json(response)).into_response();
            }
        }
    }
    (
        StatusCode::UNAUTHORIZED,
        Json(json!({"error": "invalid_token"})),
    )
        .into_response()
}

async fn error_page(Query(params): Query<HashMap<String, String>>) -> Html<String> {
    let error = params.get("error").map(|s| s.as_str()).unwrap_or("unknown");
    Html(format!("<h1>OAuth Error: {}</h1>", error))
}

fn build_cors_layer(config: &IssuerConfig) -> CorsLayer {
    let allowed_origins: Vec<HeaderValue> = config
        .allowed_origins
        .iter()
        .filter_map(|s| s.parse().ok())
        .collect();

    let allowed = if allowed_origins.is_empty() {
        AllowOrigin::any()
    } else {
        AllowOrigin::list(allowed_origins)
    };

    let allowed_methods =
        AllowMethods::list([http::Method::GET, http::Method::POST, http::Method::OPTIONS]);

    let allowed_headers = AllowHeaders::list([
        header::AUTHORIZATION,
        header::CONTENT_TYPE,
        header::ACCEPT,
        "x-requested-with".parse().unwrap(),
    ]);

    CorsLayer::new()
        .allow_origin(allowed)
        .allow_methods(allowed_methods)
        .allow_headers(allowed_headers)
        .allow_credentials(true)
        .max_age(std::time::Duration::from_secs(86400))
}
