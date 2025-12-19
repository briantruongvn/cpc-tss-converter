# GitHub Actions Keep-Alive Workflow

This document explains the automated keep-alive system that prevents the CPC TSS Converter Streamlit app from sleeping.

## Overview

The Streamlit Cloud free tier puts apps to sleep after ~12 hours of inactivity. This GitHub Actions workflow automatically pings the app every 4 hours to keep it responsive.

## Features

- ⏰ **Automated Schedule**: Runs every 4 hours
- 🔄 **Retry Logic**: 3 attempts with 30-second delays
- 📊 **Logging**: Detailed execution logs
- 🚨 **Error Handling**: Failure notifications
- 🎯 **Manual Trigger**: Can be run manually when needed

## Configuration

### Default Settings

The workflow is configured with conservative, ToS-compliant settings:

- **Schedule**: `0 */4 * * *` (every 4 hours)
- **Timeout**: 5 minutes maximum
- **Request Timeout**: 30 seconds with 10-second connection timeout
- **Retries**: 3 attempts with exponential backoff

### Custom App URL

To use a custom Streamlit app URL:

1. Go to your GitHub repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Create a new repository secret named `STREAMLIT_APP_URL`
4. Set the value to your Streamlit app URL (e.g., `https://your-app.streamlit.app`)

If no secret is configured, it defaults to `https://cpc-tss-converter.streamlit.app`

## Usage

### Automatic Operation

The workflow runs automatically every 4 hours. No manual intervention required.

### Manual Trigger

To manually trigger the workflow:

1. Go to the "Actions" tab in your GitHub repository
2. Select "Keep Streamlit App Alive" workflow
3. Click "Run workflow"
4. Optionally provide a reason for the manual trigger
5. Click "Run workflow" button

### Monitoring

Check workflow status:

1. Navigate to the "Actions" tab
2. View recent workflow runs
3. Click on any run to see detailed logs
4. Monitor success/failure patterns

## Workflow Output

### Successful Run
```
🚀 Starting keep-alive check at [timestamp]
📍 Target URL: https://cpc-tss-converter.streamlit.app
🔄 Attempt 1 of 3
✅ Success! App responded with HTTP 200
🎉 Keep-alive check completed successfully
⏰ Keep-alive check finished at [timestamp]
```

### Failed Run
```
🚀 Starting keep-alive check at [timestamp]
📍 Target URL: https://cpc-tss-converter.streamlit.app
🔄 Attempt 1 of 3
⚠️  Got HTTP response: 503
⏳ Waiting 30 seconds before retry...
🔄 Attempt 2 of 3
⚠️  Got HTTP response: 503
⏳ Waiting 30 seconds before retry...
🔄 Attempt 3 of 3
⚠️  Got HTTP response: 503
❌ Failed after 3 attempts
🚨 ALERT: Keep-alive workflow failed!
```

## Terms of Service Compliance

This workflow is designed to comply with Streamlit's terms of service:

- **Conservative Timing**: 4-hour intervals (not aggressive)
- **Standard HTTP Requests**: Mimics normal browser behavior
- **Proper Headers**: Includes appropriate user-agent and accept headers
- **Rate Limiting**: Built-in timeouts and retry limits
- **Legitimate Use**: For business application availability

## Troubleshooting

### Common Issues

1. **HTTP 503 Errors**: App deployment issues or Streamlit service problems
2. **Timeout Errors**: Network connectivity issues
3. **403/404 Errors**: Incorrect app URL configuration

### Solutions

1. **Check App Status**: Manually visit the Streamlit app URL
2. **Verify URL**: Ensure `STREAMLIT_APP_URL` secret is correct
3. **Check Logs**: Review workflow execution logs for details
4. **Manual Test**: Trigger workflow manually to test

### Disabling the Workflow

To temporarily disable the keep-alive workflow:

1. Edit `.github/workflows/keep-alive.yml`
2. Comment out the `schedule:` section:
   ```yaml
   # schedule:
   #   - cron: '0 */4 * * *'
   ```
3. Commit the changes

To re-enable, uncomment the schedule section.

## Alternatives

If the keep-alive workflow doesn't meet your needs:

1. **Streamlit Cloud Pro**: Paid plan with guaranteed uptime
2. **Alternative Hosting**: Railway, Render, Heroku, etc.
3. **External Monitors**: UptimeRobot, Pingdom services
4. **Custom Solutions**: Self-hosted monitoring scripts

## Best Practices

1. **Monitor Regularly**: Check workflow status weekly
2. **Update URLs**: Keep app URLs current in secrets
3. **Review Logs**: Investigate patterns of failures
4. **Backup Plan**: Have alternative hosting ready if needed
5. **Respect Limits**: Don't modify timing to be more aggressive

## Support

For issues with the keep-alive workflow:

1. Check GitHub Actions logs
2. Verify app deployment status
3. Review Streamlit Cloud service status
4. Test app accessibility manually

Remember: This workflow maintains app availability but doesn't guarantee 100% uptime. Consider upgrading to paid hosting for mission-critical applications.