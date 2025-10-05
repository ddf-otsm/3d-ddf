#!/usr/bin/env python3
"""
Jenkins Webhook Receiver for 3D-DDF Project

Receives GitHub webhooks and triggers appropriate Jenkins jobs based on branch and repository.
"""

import os
import json
import logging
import requests
from flask import Flask, request, jsonify
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
JENKINS_URL = os.getenv('JENKINS_URL', 'http://localhost:8080')
JENKINS_USER = os.getenv('JENKINS_USER', 'admin')
JENKINS_TOKEN = os.getenv('JENKINS_TOKEN', '')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')

# Job mapping based on branch
JOB_MAPPING = {
    'main': '3d-ddf-validation',
    'master': '3d-ddf-validation',
    'develop': '3d-ddf-validation-develop',
    'staging': '3d-ddf-validation-staging',
    'feature': '3d-ddf-validation-feature'
}

def trigger_jenkins_job(job_name, payload):
    """Trigger a Jenkins job with the given payload"""

    if not JENKINS_TOKEN:
        logger.warning("JENKINS_TOKEN not set, skipping job trigger")
        return {"status": "skipped", "reason": "no_token"}

    job_url = f"{JENKINS_URL}/job/{job_name}/build"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {JENKINS_TOKEN}'
    }

    # Prepare Jenkins parameters
    params = {
        'REPOSITORY': payload.get('repository', {}).get('name', 'unknown'),
        'BRANCH': payload.get('ref', 'refs/heads/unknown').replace('refs/heads/', ''),
        'COMMIT_SHA': payload.get('after', 'unknown'),
        'COMMIT_MESSAGE': payload.get('commits', [{}])[0].get('message', 'No message')
    }

    try:
        response = requests.post(
            job_url,
            auth=(JENKINS_USER, JENKINS_TOKEN),
            params=params,
            timeout=10
        )

        if response.status_code in [200, 201, 302]:
            logger.info(f"Successfully triggered Jenkins job: {job_name}")
            return {"status": "success", "job_name": job_name}
        else:
            logger.error(f"Failed to trigger Jenkins job {job_name}: {response.status_code}")
            return {"status": "error", "code": response.status_code}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error triggering Jenkins job {job_name}: {str(e)}")
        return {"status": "error", "reason": str(e)}

def determine_job_name(payload):
    """Determine which Jenkins job to trigger based on the payload"""

    ref = payload.get('ref', '')
    branch = ref.replace('refs/heads/', '') if ref.startswith('refs/heads/') else 'unknown'

    # Map branch to job
    for branch_pattern, job_name in JOB_MAPPING.items():
        if branch == branch_pattern or branch.startswith(f'{branch_pattern}/'):
            return job_name

    # Default to feature job for unknown branches
    return JOB_MAPPING['feature']

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "jenkins-webhook-receiver"
    })

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook payloads"""

    # Verify webhook secret if configured
    if WEBHOOK_SECRET:
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not signature.startswith('sha256='):
            return jsonify({"error": "Invalid signature format"}), 400

        import hmac
        import hashlib
        expected_signature = hmac.new(
            WEBHOOK_SECRET.encode(),
            request.get_data(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(f'sha256={expected_signature}', signature):
            return jsonify({"error": "Invalid signature"}), 401

    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No JSON payload"}), 400

        logger.info(f"Received webhook for repository: {payload.get('repository', {}).get('name', 'unknown')}")

        # Determine which job to trigger
        job_name = determine_job_name(payload)

        # Trigger the Jenkins job
        result = trigger_jenkins_job(job_name, payload)

        return jsonify({
            "status": "processed",
            "job_triggered": job_name,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/status', methods=['GET'])
def status():
    """Get webhook receiver status"""
    return jsonify({
        "status": "running",
        "jenkins_url": JENKINS_URL,
        "job_mapping": JOB_MAPPING,
        "webhook_secret_configured": bool(WEBHOOK_SECRET),
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    logger.info("Starting Jenkins webhook receiver...")
    app.run(host='0.0.0.0', port=9000, debug=True)
