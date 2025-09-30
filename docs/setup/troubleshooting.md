# Troubleshooting Guide

## Common Issues

### MCP showing red or "no tools"

**Solutions:**
1. Make sure Blender is open with the addon installed and enabled
2. In Blender, click "Connect to Claude" in the BlenderMCP sidebar panel
3. Restart Cursor after the Blender server is running
4. The MCP needs Blender to be running to connect properly

### Connection issues

- Make sure the Blender addon server is running (click "Connect to Claude" in Blender)
- Check that no firewall is blocking port 9876
- Verify Blender is running and the addon is enabled

### MCP not showing

- Restart Cursor after adding the MCP configuration
- Check `.cursor/mcp.json` is properly configured
- Look for the hammer icon 🔨 in Cursor's interface

### Timeout errors

- Try simplifying your requests or breaking them into smaller steps
- Check Blender is not busy with another operation
- Increase timeout settings if necessary

### Test failures

**"Connection refused":**
- Make sure Blender is running
- Make sure the MCP addon is installed and enabled
- Click "Connect to Claude" in the BlenderMCP panel in Blender

**"Object not found":**
- The test may have failed mid-execution
- Manually delete any test objects in Blender
- Run the test again

**"Unknown command type":**
- Make sure the addon is up to date
- Check that the Blender MCP server is version 1.2 or higher

### Still having issues?

Try these steps in order:
1. Check Blender BlenderMCP panel shows "Connected"
2. Restart the Blender MCP server (disconnect and reconnect)
3. Restart Cursor
4. Restart Blender
5. Check the Blender system console for error messages

## Important Notes

⚠️ **Security Warning**: The MCP allows running arbitrary Python code in Blender. ALWAYS save your work before using it.

⚠️ **Single Instance**: Only run one instance of the MCP server at a time (don't run it in both Cursor and Claude Desktop simultaneously).
