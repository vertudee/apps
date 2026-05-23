use colored::Colorize;
use oauth2_test_server::{IssuerConfig, OAuthTestServer};

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();
    let config = IssuerConfig {
        port: 8090,
        ..Default::default()
    };
    let server = OAuthTestServer::start_with_config(config).await;

    println!(
        "{} {}",
        "OAuth Test Server running on".green().bold(),
        server.base_url().to_string().blue().bold()
    );
    println!(" {} {}", "• Discovery:".bold(), server.endpoints.discovery);
    println!(" {} {}", "• Jwks:".bold(), server.endpoints.jwks);
    println!(" {} {}", "• Authorize:".bold(), server.endpoints.authorize);
    println!(" {} {}", "• Token:".bold(), server.endpoints.token);
    println!(" {} {}", "• Register:".bold(), server.endpoints.register);
    println!(
        " {} {}",
        "• Introspection:".bold(),
        server.endpoints.introspect
    );
    println!(" {} {}", "• UserInfo:".bold(), server.endpoints.userinfo);
    println!(" {} {}", "• Revoke:".bold(), server.endpoints.revoke);

    if let Err(err) = server.wait_for_shutdown().await {
        eprintln!("{err}");
    }
}

#[cfg(test)]
mod tests {

    #[tokio::test]
    async fn my_oauth_test() {
        let server = oauth2_test_server::OAuthTestServer::start().await;
        println!("server: {}", server.base_url());
        println!("authorize endpoint: {}", server.endpoints.authorize);
        // register a client
        let client = server.register_client(serde_json::json!({ "scope": "openid",
            "redirect_uris":["http://localhost:8080/callback"],
            "client_name": "rust-mcp-sdk"
        }));
        // generate a jwt
        let token = server.generate_token(&client, server.jwt_options().user_id("rustmcp").build());
        assert_eq!(token.access_token.split('.').count(), 3);
        assert_eq!(server.clients().read().iter().len(), 1);
        assert_eq!(server.tokens().read().iter().len(), 1);
    }
}
