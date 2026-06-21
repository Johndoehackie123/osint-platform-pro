from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from app.utils import get_ip_info, get_whois_info, get_dns_records, search_username, analyze_website
from app.optimizer import optimizer
from app.tools import get_tools_status
import time
import logging
import json

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    # Simple health check used by Render
    return jsonify({"status": "ok"}), 200

@app.route('/ip-lookup')
def ip_lookup():
    return render_template('ip_lookup.html')

@app.route('/domain-lookup')
def domain_lookup():
    return render_template('domain_lookup.html')

@app.route('/identity-lookup')
def identity_lookup():
    return render_template('identity_lookup.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/tools')
def tools_page():
    return render_template('tools.html')

@app.route('/api/ip/<ip>')
def api_ip(ip):
    try:
        logger.info("IP lookup for %s", ip)
        time.sleep(0.5)
        data = get_ip_info(ip)
        return jsonify(data)
    except Exception as e:
        logger.exception("Error in api_ip")
        return jsonify({"error": str(e)}), 500

@app.route('/api/domain/<domain>')
def api_domain(domain):
    try:
        logger.info("Domain lookup for %s", domain)
        time.sleep(0.5)
        whois_data = get_whois_info(domain)
        dns_data = get_dns_records(domain)
        return jsonify({"whois": whois_data, "dns": dns_data})
    except Exception as e:
        logger.exception("Error in api_domain")
        return jsonify({"error": str(e)}), 500

@app.route('/api/username/<username>')
def api_username(username):
    try:
        logger.info("Username search for %s", username)
        time.sleep(0.5)
        data = search_username(username)
        return jsonify(data)
    except Exception as e:
        logger.exception("Error in api_username")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze/<path:url>')
def api_analyze(url):
    try:
        logger.info("Analyze url %s", url)
        time.sleep(0.5)
        data = analyze_website(url)
        return jsonify(data)
    except Exception as e:
        logger.exception("Error in api_analyze")
        return jsonify({"error": str(e)}), 500

@app.route('/api/system-stats')
def api_system_stats():
    try:
        return jsonify(optimizer.get_stats())
    except Exception as e:
        logger.exception("Error in api_system_stats")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tools-status')
def api_tools_status():
    try:
        statuses = get_tools_status()
        return jsonify(statuses)
    except Exception as e:
        logger.exception("Error in api_tools_status")
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    try:
        msg = optimizer.optimize()
        return jsonify({"message": msg, "stats": optimizer.get_stats()})
    except Exception as e:
        logger.exception("Error in api_optimize")
        return jsonify({"error": str(e)}), 500

@app.route('/stream/stats')
def stream_stats():
    def event_stream():
        try:
            while True:
                stats = optimizer.get_stats()
                payload = json.dumps(stats)
                yield f"data: {payload}\n\n"
                time.sleep(1)
        except GeneratorExit:
            logger.info("SSE client disconnected")
    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

@app.route('/stream/tools')
def stream_tools():
    def event_stream():
        try:
            while True:
                statuses = get_tools_status(force=True)
                payload = json.dumps(statuses)
                yield f"data: {payload}\n\n"
                time.sleep(15)
        except GeneratorExit:
            logger.info("SSE tools client disconnected")
    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

# Generic error handler
@app.errorhandler(500)
def internal_error(error):
    logger.exception("Server Error: %s", error)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
