# Security Policy

## Secrets Management

**CRITICAL: Never commit secrets to this repository.**

### What are secrets?
- API keys (YouTube, OpenAI, etc.)
- OAuth tokens and refresh tokens
- Client IDs and client secrets
- Private keys and certificates
- Database credentials
- Any authentication tokens

### How we handle secrets

#### Local Development
1. Copy `.env.example` to `.env`
2. Fill in your secrets in `.env`
3. `.env` is gitignored and will never be committed

#### Production/CI
- Use cloud secret managers:
  - AWS: Secrets Manager or Parameter Store
  - Azure: Key Vault
  - GCP: Secret Manager
  - GitHub: Actions Secrets

### Reporting Security Issues

If you discover a security vulnerability, please email:
- **DO NOT** open a public issue
- Email: [your-email@example.com]
- Include: description, steps to reproduce, potential impact

### Best Practices
- Rotate secrets regularly
- Use least-privilege access
- Never log secrets
- Use environment variables, not hardcoded values

