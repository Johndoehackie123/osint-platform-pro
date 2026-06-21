from flask import Flask, render_template, request, jsonify
from app.utils import get_ip_info, get_whois_info, get_dns_records, search_username, analyze_website
from app.optimizer import optimizer
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/api/ip/<ip>')
def api_ip(ip):
    time.sleep(1) # Simulate work for progress bar
    return jsonify(get_ip_info(ip))

@app.route('/api/domain/<domain>')
def api_domain(domain):
    time.sleep(1)
    whois_data = get_whois_info(domain)
    dns_data = get_dns_records(domain)
    return jsonify({"whois": whois_data, "dns": dns_data})

@app.route('/api/username/<username>')
def api_username(username):
    # Since username search takes time, we'll simulate a phased response or just return all
    time.sleep(1)
    return jsonify(search_username(username))

@app.route('/api/analyze/<url>')
def api_analyze(url):
    time.sleep(1)
    return jsonify(analyze_website(url))

@app.route('/api/system-stats')
def api_system_stats():
    return jsonify(optimizer.get_stats())

@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    msg = optimizer.optimize()
    return jsonify({"message": msg, "stats": optimizer.get_stats()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
