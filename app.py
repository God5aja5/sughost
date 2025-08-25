from flask import Flask, request, redirect, url_for, session, jsonify
import requests
import os
from datetime import datetime, timedelta
import functools
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random
import string
import uuid
import time
from collections import defaultdict
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global config (adjustable via admin)
CONFIG = {
    'search_cost': int(os.environ.get('SEARCH_COST', 2))
}

# Rate limiting storage
registration_attempts = defaultdict(lambda: {'count': 0, 'last_attempt': 0})
api_attempts = defaultdict(lambda: {'count': 0, 'last_attempt': 0})

# In-memory database (ephemeral on serverless)
users_db = {}
keys_db = {}
search_logs_db = []
tickets_db = {}
ticket_replies_db = {}
ticket_attachments_db = {}
api_tokens = {}

# Initialize admin user
ADMIN_USERNAME = "God@Baign"
ADMIN_PASSWORD = "God@111983"

if ADMIN_USERNAME not in users_db:
    users_db[ADMIN_USERNAME] = {
        'id': str(uuid.uuid4()),
        'email': 'admin@osint.com',
        'password': generate_password_hash(ADMIN_PASSWORD),
        'credits': 999999,
        'credits_expiry': None,
        'role': 'admin',
        'created_at': datetime.now().isoformat(),
        'last_login': None,
        'ip_address': None,
        'status': 'active'
    }

# Complete Enhanced Style with Advanced Animations
COMPLETE_STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    
    :root {
        --primary-black: #050505; 
        --secondary-black: #0d0d0f; 
        --tertiary-black: #18181b;
        --primary-red: #dc2626; 
        --secondary-red: #991b1b; 
        --accent-red: #ff4444; 
        --neon-red: #ff0040;
        --text-light: #ffffff; 
        --text-gray: #9ca3af; 
        --text-dark-gray: #6b7280; 
        --border-color: #2a2a2a;
        --success-green: #22c55e; 
        --warning-yellow: #eab308; 
        --info-blue: #3b82f6;
        --purple-accent: #a855f7; 
        --pink-accent: #ec4899;
    }
    
    body { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
        background: #000; 
        min-height: 100vh; 
        color: var(--text-light); 
        position: relative; 
        overflow-x: hidden; 
    }
    
    /* Advanced Animated Background */
    .animated-bg { 
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100%; 
        z-index: 0; 
        background: radial-gradient(1200px 600px at 80% -10%, rgba(167, 139, 250, 0.15), transparent 60%), 
                    radial-gradient(900px 500px at -10% 110%, rgba(239, 68, 68, 0.15), transparent 60%), 
                    linear-gradient(135deg, #050505 0%, #0d0d0f 100%); 
    }
    
    .animated-bg::before {
        content: ''; 
        position: absolute; 
        inset: 0;
        background-image: radial-gradient(circle at 20% 80%, rgba(220, 38, 38, 0.1) 0%, transparent 50%), 
                         radial-gradient(circle at 80% 20%, rgba(168, 85, 247, 0.08) 0%, transparent 50%), 
                         radial-gradient(circle at 40% 40%, rgba(236, 72, 153, 0.06) 0%, transparent 50%);
        animation: gradientShift 16s ease-in-out infinite;
    }
    
    @keyframes gradientShift { 
        0%, 100% { transform: translate(0,0) rotate(0) }
        33% { transform: translate(-20px,-20px) rotate(120deg) }
        66% { transform: translate(20px,-20px) rotate(240deg) }
    }
    
    /* Grid Animation */
    .grid-animation { 
        position: absolute; 
        inset: 0; 
        background-image: linear-gradient(rgba(220,38,38,0.03) 1px, transparent 1px), 
                         linear-gradient(90deg, rgba(220,38,38,0.03) 1px, transparent 1px); 
        background-size: 50px 50px; 
        animation: gridMove 20s linear infinite; 
    }
    
    @keyframes gridMove { 
        0% { transform: translate(0,0) }
        100% { transform: translate(50px,50px) }
    }
    
    /* Particle Effects */
    .floating-particles { 
        position: absolute; 
        inset: 0; 
        overflow: hidden; 
        pointer-events: none; 
    }
    
    .particle { 
        position: absolute; 
        width: 4px; 
        height: 4px; 
        background: rgba(220,38,38,0.5); 
        border-radius: 50%; 
        animation: float 20s infinite; 
    }
    
    .particle:nth-child(odd) { 
        width: 2px; 
        height: 2px; 
        animation-duration: 26s; 
        background: rgba(168,85,247,0.5); 
    }
    
    .glyph { 
        position: absolute; 
        color: rgba(255,255,255,0.09); 
        font-size: 18px; 
        user-select: none; 
        animation: float 24s infinite; 
        text-shadow: 0 0 8px rgba(255,255,255,0.1), 0 0 20px rgba(236,72,153,0.15); 
    }
    
    @keyframes float { 
        0% { transform: translateY(100vh) translateX(0) scale(0.7); opacity: 0; }
        10% { opacity: .9; transform: scale(1); }
        90% { opacity: .9; }
        100% { transform: translateY(-100vh) translateX(120px) scale(0.7); opacity: 0; }
    }
    
    /* Layout */
    .container { 
        max-width: 1400px; 
        margin: 0 auto; 
        padding: 20px; 
        position: relative; 
        z-index: 2; 
    }
    
    /* Header Styles */
    .header { 
        background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); 
        padding: 40px; 
        border-radius: 25px; 
        margin-bottom: 40px; 
        border: 1px solid rgba(220,38,38,0.2); 
        backdrop-filter: blur(20px);
        animation: slideDown 0.6s ease;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .header h1 { 
        font-size: 3.2rem; 
        font-weight: 900; 
        background: linear-gradient(135deg, var(--primary-red), var(--accent-red), var(--purple-accent)); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        margin-bottom: 10px; 
        text-transform: uppercase; 
        letter-spacing: 3px;
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    /* Credits Display */
    .credits-display { 
        position: fixed; 
        top: 20px; 
        left: 20px; 
        background: linear-gradient(135deg, rgba(34,197,94,0.25), rgba(34,197,94,0.1)); 
        padding: 12px 24px; 
        border-radius: 15px; 
        border: 1px solid rgba(34,197,94,0.3); 
        backdrop-filter: blur(20px); 
        z-index: 1000; 
        animation: pulse 2s ease infinite;
        transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
    }
    
    .credits-display:hover {
        transform: scale(1.05);
    }
    
    @keyframes pulse { 
        0%, 100% { transform: scale(1) }
        50% { transform: scale(1.02) }
    }
    
    /* User Info Bar */
    .user-info { 
        position: fixed; 
        top: 20px; 
        right: 20px; 
        background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); 
        padding: 12px 24px; 
        border-radius: 15px; 
        border: 1px solid rgba(220,38,38,0.2); 
        backdrop-filter: blur(20px); 
        z-index: 1000; 
        display: flex; 
        align-items: center; 
        gap: 15px; 
        flex-wrap: wrap;
        animation: slideLeft 0.6s ease;
    }
    
    @keyframes slideLeft {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Tools Grid */
    .tools-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
        gap: 30px; 
        margin-top: 40px; 
    }
    
    .tool-card { 
        background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); 
        padding: 35px; 
        border-radius: 20px; 
        border: 1px solid rgba(220,38,38,0.1); 
        transition: all .4s cubic-bezier(.4,0,.2,1); 
        cursor: pointer; 
        position: relative; 
        overflow: hidden; 
        text-decoration: none; 
        display: block;
        animation: fadeUp 0.6s ease forwards;
        opacity: 0;
    }
    
    .tool-card:nth-child(1) { animation-delay: 0.1s; }
    .tool-card:nth-child(2) { animation-delay: 0.2s; }
    .tool-card:nth-child(3) { animation-delay: 0.3s; }
    .tool-card:nth-child(4) { animation-delay: 0.4s; }
    .tool-card:nth-child(5) { animation-delay: 0.5s; }
    .tool-card:nth-child(6) { animation-delay: 0.6s; }
    
    @keyframes fadeUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .tool-card::before { 
        content: ''; 
        position: absolute; 
        inset: 0; 
        background: linear-gradient(135deg, rgba(220,38,38,0.1), transparent); 
        opacity: 0; 
        transition: opacity .3s ease; 
    }
    
    .tool-card:hover::before { opacity: 1; }
    
    .tool-card:hover { 
        transform: translateY(-8px) scale(1.02); 
        box-shadow: 0 20px 40px rgba(220,38,38,0.3); 
        border-color: rgba(220,38,38,0.4); 
    }
    
    /* Search Container */
    .search-container { 
        background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); 
        padding: 50px; 
        border-radius: 25px; 
        border: 1px solid rgba(220,38,38,0.2); 
        margin-bottom: 40px; 
        backdrop-filter: blur(20px);
        animation: slideUp 0.6s ease;
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .search-form { 
        display: flex; 
        gap: 15px; 
        max-width: 700px; 
        margin: 0 auto; 
    }
    
    .search-input { 
        flex: 1; 
        padding: 18px 24px; 
        background: rgba(10,10,10,0.8); 
        border: 1px solid rgba(220,38,38,0.2); 
        border-radius: 15px; 
        color: var(--text-light); 
        font-size: 1.05rem; 
        transition: all .3s cubic-bezier(.4,0,.2,1); 
    }
    
    .search-input:focus {
        outline: none;
        border-color: var(--primary-red);
        box-shadow: 0 0 0 3px rgba(220,38,38,0.1);
    }
    
    .search-btn { 
        padding: 18px 36px; 
        background: linear-gradient(135deg, var(--primary-red), var(--secondary-red)); 
        color: #fff; 
        border: none; 
        border-radius: 15px; 
        font-size: 1.05rem; 
        font-weight: 600; 
        cursor: pointer; 
        transition: all .3s cubic-bezier(.4,0,.2,1); 
        text-transform: uppercase; 
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .search-btn::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .search-btn:active::after {
        width: 300px;
        height: 300px;
    }
    
    .search-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(220,38,38,0.4);
    }
    
    /* Results Container */
    .results-container { 
        background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); 
        padding: 50px; 
        border-radius: 25px; 
        border: 1px solid rgba(220,38,38,0.2); 
        backdrop-filter: blur(20px);
        animation: fadeIn 0.6s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .result-item { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 20px 25px; 
        background: linear-gradient(135deg, rgba(10,10,10,0.9), rgba(10,10,10,0.7)); 
        border-radius: 15px; 
        margin-bottom: 15px; 
        border: 1px solid rgba(220,38,38,0.1); 
        transition: all .3s cubic-bezier(.4,0,.2,1);
        animation: slideRight 0.4s ease;
    }
    
    @keyframes slideRight {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .result-item:hover {
        transform: translateX(5px);
        border-color: rgba(220,38,38,0.3);
        box-shadow: 0 5px 15px rgba(220,38,38,0.2);
    }
    
    /* Loading Animation */
    .loading {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px;
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(220,38,38,0.1);
        border-top-color: var(--primary-red);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .loading p {
        margin-top: 20px;
        color: var(--text-gray);
        animation: blink 1.5s ease infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Forms */
    .form-group { 
        margin-bottom: 20px; 
    }
    
    .form-group label { 
        display: block; 
        margin-bottom: 8px; 
        color: var(--text-gray); 
        font-size: .9rem; 
        font-weight: 500; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
    }
    
    .form-group input, 
    .form-group select, 
    .form-group textarea { 
        width: 100%; 
        padding: 14px 18px; 
        background: rgba(10,10,10,0.8); 
        border: 1px solid rgba(220,38,38,0.2); 
        border-radius: 12px; 
        color: var(--text-light); 
        font-size: 1rem; 
        transition: all .3s cubic-bezier(.4,0,.2,1); 
    }
    
    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
        outline: none;
        border-color: var(--primary-red);
        box-shadow: 0 0 0 3px rgba(220,38,38,0.1);
    }
    
    /* Buttons */
    .btn { 
        padding: 14px 30px; 
        background: linear-gradient(135deg, var(--primary-red), var(--secondary-red)); 
        color: #fff; 
        border: none; 
        border-radius: 12px; 
        font-size: 1rem; 
        font-weight: 600; 
        cursor: pointer; 
        transition: all .3s cubic-bezier(.4,0,.2,1); 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        position: relative; 
        overflow: hidden; 
    }
    
    .btn:hover { 
        transform: translateY(-3px) scale(1.02); 
        box-shadow: 0 10px 30px rgba(220,38,38,0.5); 
    }
    
    .btn-alt { 
        background: linear-gradient(135deg, #374151, #1f2937); 
    }
    
    /* Copy Button */
    .copy-btn {
        padding: 6px 12px;
        font-size: .8rem;
        background: linear-gradient(135deg, var(--primary-red), var(--secondary-red));
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-left: 10px;
    }
    
    .copy-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(220,38,38,0.4);
    }
    
    .copy-btn:active {
        transform: scale(0.95);
    }
    
    .copy-btn.copied {
        background: linear-gradient(135deg, var(--success-green), #16a34a);
    }
    
    /* Data Display */
    .data-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .data-card {
        background: rgba(10,10,10,0.5);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(220,38,38,0.1);
        transition: all 0.3s ease;
    }
    
    .data-card:hover {
        transform: translateY(-2px);
        border-color: rgba(220,38,38,0.3);
    }
    
    .data-label {
        color: var(--text-gray);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    .data-value {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        word-break: break-word;
    }
    
    /* Status Badges */
    .status-badge { 
        padding: 4px 10px; 
        border-radius: 12px; 
        font-size: .8rem; 
        font-weight: 600; 
        text-transform: uppercase; 
    }
    
    .status-active { 
        background: rgba(34,197,94,0.2); 
        color: var(--success-green); 
        border: 1px solid rgba(34,197,94,0.3); 
    }
    
    /* Pills */
    .pill { 
        padding: 4px 10px; 
        border-radius: 999px; 
        font-size: .85rem; 
        border: 1px solid transparent; 
    }
    
    .pill-yes { 
        background: rgba(34,197,94,0.2); 
        color: var(--success-green); 
        border-color: rgba(34,197,94,0.3); 
    }
    
    .pill-no { 
        background: rgba(220,38,38,0.2); 
        color: var(--primary-red); 
        border-color: rgba(220,38,38,0.3); 
    }
    
    /* Pricing Cards */
    .pricing-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
        gap: 30px; 
        margin-top: 40px; 
    }
    
    .pricing-card { 
        background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); 
        padding: 35px; 
        border-radius: 20px; 
        border: 1px solid rgba(220,38,38,0.2); 
        text-align: center; 
        transition: all .4s cubic-bezier(.4,0,.2,1);
        animation: fadeUp 0.6s ease forwards;
        opacity: 0;
    }
    
    .pricing-card:nth-child(1) { animation-delay: 0.1s; }
    .pricing-card:nth-child(2) { animation-delay: 0.2s; }
    .pricing-card:nth-child(3) { animation-delay: 0.3s; }
    
    .pricing-card.featured { 
        border: 2px solid var(--primary-red); 
        transform: scale(1.05);
        animation-delay: 0.2s;
    }
    
    .pricing-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(220,38,38,0.3);
    }
    
    /* Table Styles */
    .admin-users-table { 
        width: 100%; 
        overflow-x: auto; 
        margin-top: 20px; 
    }
    
    .admin-users-table table { 
        width: 100%; 
        border-collapse: collapse; 
        min-width: 840px; 
    }
    
    .admin-users-table th { 
        background: linear-gradient(135deg, rgba(220,38,38,0.1), rgba(220,38,38,0.05)); 
        color: var(--primary-red); 
        padding: 15px; 
        text-align: left; 
        font-weight: 600; 
        text-transform: uppercase; 
        font-size: .85rem; 
        letter-spacing: 1px; 
        border-bottom: 2px solid rgba(220,38,38,0.2); 
    }
    
    .admin-users-table td { 
        padding: 15px; 
        border-bottom: 1px solid rgba(220,38,38,0.1); 
        color: var(--text-light); 
        font-size: .95rem; 
    }
    
    /* Ticket Card */
    .ticket-card { 
        background: linear-gradient(135deg, rgba(10,10,10,0.9), rgba(10,10,10,0.7)); 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid rgba(220,38,38,0.1); 
        transition: all .3s ease; 
        cursor: pointer; 
        margin-bottom: 20px; 
    }
    
    .ticket-card:hover {
        transform: translateX(5px);
        border-color: rgba(220,38,38,0.3);
        box-shadow: 0 5px 15px rgba(220,38,38,0.2);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .container { 
            padding: 10px; 
        }
        
        .header h1 { 
            font-size: 2rem; 
        }
        
        .header {
            padding: 25px;
        }
        
        .tools-grid { 
            grid-template-columns: 1fr; 
            gap: 20px;
        }
        
        .search-form { 
            flex-direction: column; 
        }
        
        .credits-display, 
        .user-info { 
            position: static; 
            margin-bottom: 20px; 
            width: 100%; 
        }
        
        .user-info {
            justify-content: center;
        }
        
        .pricing-grid { 
            grid-template-columns: 1fr; 
        }
        
        .pricing-card.featured {
            transform: scale(1);
        }
        
        .search-container {
            padding: 30px 20px;
        }
        
        .results-container {
            padding: 30px 20px;
        }
        
        .data-grid {
            grid-template-columns: 1fr;
        }
        
        .admin-users-table {
            overflow-x: scroll;
        }
    }
    
    @media (max-width: 480px) {
        .header h1 {
            font-size: 1.5rem;
            letter-spacing: 1px;
        }
        
        .tool-card {
            padding: 25px;
        }
        
        .search-btn {
            padding: 16px 24px;
        }
    }
</style>
'''

# Enhanced Global Script with Better Data Handling
GLOBAL_SCRIPT = '''
<script>
// Format timestamp
function formatTimestamp(val){
  try{
    const n = Number(val);
    if(!Number.isFinite(n)) return null;
    const ms = (n > 1e12) ? n : (n > 1e9 ? n*1000 : null);
    if (!ms) return null;
    const d = new Date(ms);
    return isNaN(d) ? null : d.toLocaleString();
  } catch(e){ return null; }
}

// Escape HTML
function escapeHtml(s){ 
    return (''+s).replace(/[&<>"']/g, m=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[m]));
}

// Convert value to display string
function toDisplayString(v){
  if (v === null || v === undefined) return '';
  if (typeof v === 'boolean') return v ? 'Yes' : 'No';
  if (typeof v === 'number') {
    const ts = formatTimestamp(v);
    return ts || String(v);
  }
  if (typeof v === 'string') {
    const maybeNum = Number(v);
    if (!isNaN(maybeNum)) {
      const ts = formatTimestamp(maybeNum);
      if (ts) return ts;
    }
    return v;
  }
  return JSON.stringify(v, null, 2);
}

// Copy text with feedback
function copyText(text, btn){
  navigator.clipboard.writeText(text).then(() => {
    if(btn) {
      const originalText = btn.innerHTML;
      btn.innerHTML = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.classList.remove('copied');
      }, 2000);
    }
  }).catch(()=>{});
}

// Filter out unwanted keys
function filterData(obj) {
  const unwantedKeys = ['dev', 'channel', '_resolved_region'];
  const filtered = {};
  for (const [key, value] of Object.entries(obj)) {
    if (!unwantedKeys.includes(key.toLowerCase())) {
      filtered[key] = value;
    }
  }
  return filtered;
}

// Render key-value pair
function renderKV(key, value){
  let valueType = typeof value;
  let display = toDisplayString(value);
  let isComplex = value && (valueType === 'object');
  
  // Skip dev/channel info
  if (['dev', 'channel'].includes(key.toLowerCase())) return '';
  
  let html = '<div class="result-item">';
  html += '<span style="color: var(--text-gray);">' + escapeHtml(key) + '</span>';
  
  if (isComplex){
    const filtered = filterData(value);
    html += '<span style="color: white; max-width: 70%; flex: 1; text-align: right;">'
         + '<details style="text-align:left;"><summary style="cursor:pointer; color: var(--info-blue);">View details (' 
         + (Array.isArray(value)? 'Array['+value.length+']':'Object') + ')</summary>'
         + '<pre style="margin-top:10px; white-space:pre-wrap; font-size:0.85rem; color: var(--text-gray);">' 
         + escapeHtml(JSON.stringify(filtered, null, 2)) + '</pre></details></span>';
    html += '<button class="copy-btn" onclick="copyText(' + JSON.stringify(JSON.stringify(filtered)) + ', this)">Copy</button>';
  } else {
    const disp = String(display);
    const pill = (typeof value === 'boolean')
      ? ('<span class="pill ' + (value?'pill-yes':'pill-no') + '">' + disp + '</span>')
      : escapeHtml(disp);
    html += '<span style="color: white; max-width:70%; text-align:right; word-break: break-word;">' + pill + '</span>';
    html += '<button class="copy-btn" onclick="copyText(' + JSON.stringify(disp) + ', this)">Copy</button>';
  }
  html += '</div>';
  return html;
}

// Render object with filtering
function renderObject(obj){
  let out = '';
  const filtered = filterData(obj);
  Object.entries(filtered).forEach(([k,v])=>{
    if (v !== null && v !== undefined && v !== '') {
      const kvHtml = renderKV(k, v);
      if (kvHtml) out += kvHtml;
    }
  });
  return out;
}

// Create data card for summary
function createDataCard(label, value) {
  return '<div class="data-card"><div class="data-label">' + escapeHtml(label) + '</div><div class="data-value">' + escapeHtml(value || '-') + '</div></div>';
}
</script>
'''

def get_base_template(title, content, include_particles=True):
    particles_html = ''
    if include_particles:
        dots = []
        for _ in range(18):
            dots.append('<div class="particle" style="left: ' + str(random.randint(0, 100)) + '%; animation-delay: ' + str(random.randint(0, 20)) + 's;"></div>')
        glyphs_chars = ['ア','ニ','メ','力','神','炎','風','光','ナ','カ','ラ','サ','タ','ハ','ひ','ネ']
        glyphs = []
        for _ in range(14):
            g = random.choice(glyphs_chars)
            glyphs.append('<div class="glyph" style="left:' + str(random.randint(0, 100)) + '%; animation-delay:' + str(random.randint(0, 18)) + 's;">' + g + '</div>')
        particles_html = '<div class="floating-particles">' + ''.join(dots + glyphs) + '</div>'
    
    return (
        '<!DOCTYPE html><html lang="en"><head>'
        '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>' + title + '</title>'
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">'
        + COMPLETE_STYLE +
        '</head><body>'
        '<div class="animated-bg"><div class="grid-animation"></div>' + particles_html + '</div>'
        '<div class="container">' + content + '</div>'
        + GLOBAL_SCRIPT +
        '</body></html>'
    )

# Helpers
def generate_key():
    chars = string.ascii_uppercase + string.digits
    return "OSIT-" + ''.join(random.choices(chars, k=4)) + "-" + ''.join(random.choices(chars, k=4))

def check_credits(username, required=None):
    if required is None:
        required = CONFIG['search_cost']
    if username in users_db:
        user = users_db[username]
        check_credits_expiry(username)
        return user.get('credits', 0) >= required
    return False

def deduct_credits(username, amount=None):
    if amount is None:
        amount = CONFIG['search_cost']
    if username in users_db:
        users_db[username]['credits'] = max(0, users_db[username].get('credits', 0) - amount)
        return True
    return False

def add_search_log(username, search_type, query, success=True, credits_used=None):
    if credits_used is None:
        credits_used = CONFIG['search_cost'] if success else 0
    search_logs_db.append({
        'id': str(uuid.uuid4()),
        'username': username,
        'type': search_type,
        'query': query,
        'success': success,
        'credits': credits_used,
        'timestamp': datetime.now().isoformat()
    })

def rate_limit_check(ip, limit_type='registration'):
    current_time = time.time()
    if limit_type == 'registration':
        attempts = registration_attempts[ip]; max_attempts = 3; time_window = 3600
    else:
        attempts = api_attempts[ip]; max_attempts = 100; time_window = 60
    if current_time - attempts['last_attempt'] > time_window:
        attempts['count'] = 0
    if attempts['count'] >= max_attempts:
        return False
    attempts['count'] += 1
    attempts['last_attempt'] = current_time
    return True

def check_credits_expiry(username):
    if username in users_db:
        user = users_db[username]
        if user.get('credits_expiry'):
            try:
                expiry_date = datetime.fromisoformat(user['credits_expiry'])
                if datetime.now() > expiry_date:
                    user['credits'] = 0
                    user['credits_expiry'] = None
                    return False
            except Exception:
                pass
        return True
    return False

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        if users_db.get(session['username'], {}).get('status') == 'banned':
            session.clear()
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        if users_db.get(session['username'], {}).get('role') != 'admin':
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username in users_db:
            user = users_db[username]
            if user.get('status') == 'banned':
                error = 'Account banned. Contact support.'
            elif check_password_hash(user['password'], password):
                session['username'] = username
                session.permanent = True
                user['last_login'] = datetime.now().isoformat()
                user['ip_address'] = request.remote_addr
                check_credits_expiry(username)
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid password'
        else:
            error = 'User not found'
        content = (
            '<div style="max-width: 420px; margin: 100px auto; background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); padding: 40px; border-radius: 25px; border: 1px solid rgba(220, 38, 38, 0.2); backdrop-filter: blur(20px);">'
            '<div style="text-align: center; margin-bottom: 30px;">'
            '<h1 style="font-size: 2.5rem; font-weight: 900; background: linear-gradient(135deg, var(--primary-red), var(--accent-red)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">OSINT Tool</h1>'
            '<p style="color: var(--text-gray);">Secure Intelligence Dashboard</p></div>'
            '<form method="POST">'
            '<div class="form-group"><label>Username</label><input type="text" name="username" required></div>'
            '<div class="form-group"><label>Password</label><input type="password" name="password" required></div>'
            '<button type="submit" class="btn" style="width: 100%;">Login</button></form>'
            '<div style="text-align: center; margin-top: 20px;"><a href="/register" style="color: var(--primary-red);">Create Account</a></div>'
            '<div style="background: rgba(220, 38, 38, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px; color: var(--primary-red);">' + error + '</div>'
            '</div>'
        )
        return get_base_template('Login - OSINT Tool', content)
    content = '''
    <div style="max-width: 420px; margin: 100px auto; background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 40px; border-radius: 25px; border: 1px solid rgba(220, 38, 38, 0.2); backdrop-filter: blur(20px);">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 2.5rem; font-weight: 900; background: linear-gradient(135deg, var(--primary-red), var(--accent-red)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">OSINT Tool</h1>
            <p style="color: var(--text-gray);">Secure Intelligence Dashboard</p>
        </div>
        <form method="POST">
            <div class="form-group"><label>Username</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Password</label><input type="password" name="password" required></div>
            <button type="submit" class="btn" style="width: 100%;">Login</button>
        </form>
        <div style="text-align: center; margin-top: 20px;"><a href="/register" style="color: var(--primary-red);">Create Account</a></div>
    </div>
    '''
    return get_base_template('Login - OSINT Tool', content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ip_address = request.remote_addr
        if not rate_limit_check(ip_address, 'registration'):
            error = 'Too many attempts. Try again later.'
        else:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
                error = 'Invalid username (3-20 characters, alphanumeric)'
            elif username in users_db:
                error = 'Username already exists'
            elif any(u.get('email') == email for u in users_db.values()):
                error = 'Email already registered'
            elif len(password) < 6:
                error = 'Password must be at least 6 characters'
            else:
                users_db[username] = {
                    'id': str(uuid.uuid4()),
                    'email': email,
                    'password': generate_password_hash(password),
                    'credits': 0,
                    'credits_expiry': None,
                    'role': 'user',
                    'created_at': datetime.now().isoformat(),
                    'last_login': None,
                    'ip_address': ip_address,
                    'status': 'active'
                }
                content = '''
                <div style="max-width: 420px; margin: 100px auto; background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 40px; border-radius: 25px;">
                    <div style="text-align: center;">
                        <h2 style="color: var(--success-green);">Registration Successful!</h2>
                        <p style="color: var(--text-gray); margin: 20px 0;">Login to access the dashboard.</p>
                        <a href="/login" class="btn">Go to Login</a>
                    </div>
                </div>
                '''
                return get_base_template('Success - OSINT Tool', content)
        content = (
            '<div style="max-width: 420px; margin: 100px auto; background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 40px; border-radius: 25px;">'
            '<div style="text-align: center; margin-bottom: 30px;"><h1 style="font-size: 2.2rem; font-weight: 900; background: linear-gradient(135deg, var(--primary-red), var(--accent-red)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Register</h1></div>'
            '<form method="POST">'
            '<div class="form-group"><label>Username</label><input type="text" name="username" required></div>'
            '<div class="form-group"><label>Email</label><input type="email" name="email" required></div>'
            '<div class="form-group"><label>Password</label><input type="password" name="password" minlength="6" required></div>'
            '<button type="submit" class="btn" style="width: 100%;">Register</button></form>'
            '<div style="background: rgba(220, 38, 38, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px; color: var(--primary-red);">' + error + '</div>'
            '</div>'
        )
        return get_base_template('Register - OSINT Tool', content)
    content = '''
    <div style="max-width: 420px; margin: 100px auto; background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 40px; border-radius: 25px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 2.2rem; font-weight: 900; background: linear-gradient(135deg, var(--primary-red), var(--accent-red)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Register</h1>
        </div>
        <form method="POST">
            <div class="form-group"><label>Username</label><input type="text" name="username" pattern="[a-zA-Z0-9_]{3,20}" required></div>
            <div class="form-group"><label>Email</label><input type="email" name="email" required></div>
            <div class="form-group"><label>Password (min 6 chars)</label><input type="password" name="password" minlength="6" required></div>
            <button type="submit" class="btn" style="width: 100%;">Register</button>
        </form>
        <div style="text-align: center; margin-top: 20px;"><a href="/login" style="color: var(--primary-red);">Already have account?</a></div>
    </div>
    '''
    return get_base_template('Register - OSINT Tool', content)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = users_db.get(session['username'], {})
    check_credits_expiry(session['username'])
    credits_expiry = ''
    if user.get('credits_expiry'):
        try:
            expiry = datetime.fromisoformat(user['credits_expiry'])
            credits_expiry = "<div style='font-size: 0.8rem; color: var(--warning-yellow);'>Expires: " + expiry.strftime('%Y-%m-%d') + "</div>"
        except Exception:
            pass
    content = (
        '<div class="credits-display"><div>Credits: <span style="color: var(--success-green); font-size: 1.2rem; font-weight: 700;">'
        + str(user.get('credits', 0)) + '</span></div>' + credits_expiry + '<div style="font-size:.8rem;color:var(--text-gray);margin-top:6px;">Per search: ' + str(CONFIG['search_cost']) + ' credits</div></div>'
        '<div class="user-info">'
        '<span>Welcome, ' + session['username'] + '</span>'
        '<a href="/profile" style="padding: 8px 15px; background: rgba(220, 38, 38, 0.2); border-radius: 8px; color: white; text-decoration: none;">Profile</a>'
        '<a href="/pricing" style="padding: 8px 15px; background: rgba(220, 38, 38, 0.2); border-radius: 8px; color: white; text-decoration: none;">Pricing</a>'
        '<a href="/tickets" style="padding: 8px 15px; background: rgba(220, 38, 38, 0.2); border-radius: 8px; color: white; text-decoration: none;">Support</a>'
        + ('<a href="/admin" style="padding: 8px 15px; background: rgba(168, 85, 247, 0.3); border-radius: 8px; color: white; text-decoration: none;">Admin</a>' if user.get('role') == 'admin' else '')
        + '<a href="/logout" style="padding: 8px 15px; background: linear-gradient(135deg, var(--primary-red), var(--secondary-red)); border-radius: 8px; color: white; text-decoration: none;">Logout</a>'
        '</div>'
        '<div style="margin-top: 80px;"><div class="header"><h1>OSINT Tool</h1>'
        '<p style="color: var(--text-gray);">Advanced Information Gathering Platform</p></div>'
        '<div class="tools-grid">'
        '<a href="/vehicle-info" class="tool-card"><i class="fas fa-car" style="font-size: 3rem; color: var(--primary-red); margin-bottom: 20px;"></i><h3 style="color: white; margin-bottom: 10px;">Vehicle Information</h3><p style="color: var(--text-gray);">Get vehicle details using registration number</p></a>'
        '<a href="/ifsc-info" class="tool-card"><i class="fas fa-university" style="font-size: 3rem; color: var(--primary-red); margin-bottom: 20px;"></i><h3 style="color: white; margin-bottom: 10px;">IFSC Lookup</h3><p style="color: var(--text-gray);">Find bank branch details using IFSC code</p></a>'
        '<a href="/pincode-info" class="tool-card"><i class="fas fa-map-marker-alt" style="font-size: 3rem; color: var(--primary-red); margin-bottom: 20px;"></i><h3 style="color: white; margin-bottom: 10px;">PIN Code Info</h3><p style="color: var(--text-gray);">Get location details from PIN code</p></a>'
        '<a href="/ip-info" class="tool-card"><i class="fas fa-globe" style="font-size: 3rem; color: var(--primary-red); margin-bottom: 20px;"></i><h3 style="color: white; margin-bottom: 10px;">IP Information</h3><p style="color: var(--text-gray);">Geolocation and ISP information</p></a>'
        '<a href="/phone-info" class="tool-card"><i class="fas fa-phone" style="font-size: 3rem; color: var(--primary-red); margin-bottom: 20px;"></i><h3 style="color: white; margin-bottom: 10px;">Phone Lookup</h3><p style="color: var(--text-gray);">Get phone number information</p></a>'
        '<a href="/freefire-info" class="tool-card"><i class="fas fa-gamepad" style="font-size: 3rem; color: var(--primary-red); margin-bottom: 20px;"></i><h3 style="color: white; margin-bottom: 10px;">FreeFire Stats</h3><p style="color: var(--text-gray);">Player statistics and information</p></a>'
        '</div></div>'
    )
    return get_base_template('Dashboard - OSINT Tool', content)

def cost_banner():
    return '<div style="text-align:center; color:var(--text-gray); margin-bottom:10px;">Each search costs <b>' + str(CONFIG['search_cost']) + '</b> credits</div>'

# Enhanced Info Pages
@app.route('/vehicle-info')
@login_required
def vehicle_info():
    if not check_credits(session['username']):
        return redirect(url_for('pricing'))
    content = (
    '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
    '<div class="search-container">'
    '<h2 style="color: var(--primary-red); text-align: center; margin-bottom: 10px;"><i class="fas fa-car"></i> Vehicle Information Search</h2>'
    + cost_banner() +
    '<form class="search-form" onsubmit="searchVehicle(event)"><input type="text" class="search-input" id="vehicleNumber" placeholder="Enter vehicle number (e.g., MH01AB1234)" required><button type="submit" class="search-btn">Search</button></form>'
    '</div><div id="results"></div>'
    '<script>'
    'async function searchVehicle(e){ e.preventDefault(); const vehicleNumber=document.getElementById("vehicleNumber").value.toUpperCase(); const resultsDiv=document.getElementById("results"); resultsDiv.innerHTML = \'<div class="loading"><div class="loading-spinner"></div><p>Searching vehicle database...</p></div>\';'
    'try{ const response=await fetch("/api/vehicle/"+vehicleNumber); const data=await response.json();'
    ' if(response.ok && data.d){ const info=filterData(data.d); let html=\'<div class="results-container"><h3 style="margin-bottom:20px;">Vehicle Details</h3>\';'
    ' html+=\'<div class="data-grid">\''
    ' + createDataCard("Registration", info.regNo || info.vehicleNumber || vehicleNumber)'
    ' + createDataCard("Owner", info.owner || "-")'
    ' + createDataCard("Model", info.model || "-")'
    ' + createDataCard("Registration Date", info.regDate || "-")'
    ' + createDataCard("Fuel Type", info.type || "-")'
    ' + createDataCard("Class", info.class || "-")'
    ' + createDataCard("Engine No", info.engine || "-")'
    ' + createDataCard("Chassis No", info.chassis || "-")'
    ' + createDataCard("RTO", info.regAuthority || "-")'
    ' + createDataCard("Status", info.status || "-")'
    ' + createDataCard("Insurance Valid Till", info.vehicleInsuranceUpto || "-")'
    ' + createDataCard("Color", info.vehicleColour || "-")'
    ' + \'</div>\';'
    ' html += \'<div style="margin-top:30px;"><h4 style="color: var(--primary-red); margin-bottom:15px;">Complete Information</h4>\' + renderObject(info) + \'</div></div>\';'
    ' resultsDiv.innerHTML = html; } else { resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-exclamation-circle"></i> No data found for this vehicle number</div>\'; }'
    '} catch(err){ resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-times-circle"></i> Error occurred while searching</div>\'; } }'
    '</script>'
    )
    return get_base_template('Vehicle Search - OSINT Tool', content, False)

@app.route('/ifsc-info')
@login_required
def ifsc_info():
    if not check_credits(session['username']):
        return redirect(url_for('pricing'))
    content = (
    '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
    '<div class="search-container">'
    '<h2 style="color: var(--primary-red); text-align: center; margin-bottom: 10px;"><i class="fas fa-university"></i> IFSC Code Lookup</h2>'
    + cost_banner() +
    '<form class="search-form" onsubmit="searchIFSC(event)"><input type="text" class="search-input" id="ifscCode" placeholder="Enter IFSC code (e.g., SBIN0000300)" required><button type="submit" class="search-btn">Search</button></form>'
    '</div><div id="results"></div>'
    '<script>'
    'async function searchIFSC(e){ e.preventDefault(); const ifsc=document.getElementById("ifscCode").value.toUpperCase(); const resultsDiv=document.getElementById("results"); resultsDiv.innerHTML = \'<div class="loading"><div class="loading-spinner"></div><p>Looking up bank details...</p></div>\';'
    'try{ const response=await fetch("/api/ifsc/"+ifsc); const data=await response.json();'
    ' if(response.ok && data.d){ const info=filterData(data.d); let html=\'<div class="results-container"><h3 style="margin-bottom:20px;">Bank Branch Details</h3>\';'
    ' html+=\'<div class="data-grid">\''
    ' + createDataCard("Bank", info.BANK || "-")'
    ' + createDataCard("Branch", info.BRANCH || "-")'
    ' + createDataCard("IFSC", info.IFSC || ifsc)'
    ' + createDataCard("MICR", info.MICR || "-")'
    ' + createDataCard("City", info.CITY || "-")'
    ' + createDataCard("District", info.DISTRICT || "-")'
    ' + createDataCard("State", info.STATE || "-")'
    ' + createDataCard("Address", info.ADDRESS || "-")'
    ' + createDataCard("Contact", info.CONTACT || "-")'
    ' + createDataCard("SWIFT", info.SWIFT || "-")'
    ' + createDataCard("UPI", info.UPI ? "Available" : "Not Available")'
    ' + createDataCard("RTGS", info.RTGS ? "Available" : "Not Available")'
    ' + \'</div>\';'
    ' html += \'<div style="margin-top:30px;"><h4 style="color: var(--primary-red); margin-bottom:15px;">All Details</h4>\' + renderObject(info) + \'</div></div>\';'
    ' resultsDiv.innerHTML = html; } else { resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-exclamation-circle"></i> Invalid IFSC code</div>\'; }'
    '} catch(err){ resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-times-circle"></i> Error occurred while searching</div>\'; } }'
    '</script>'
    )
    return get_base_template('IFSC Lookup - OSINT Tool', content, False)

@app.route('/pincode-info')
@login_required
def pincode_info():
    if not check_credits(session['username']):
        return redirect(url_for('pricing'))
    content = (
    '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
    '<div class="search-container">'
    '<h2 style="color: var(--primary-red); text-align: center; margin-bottom: 10px;"><i class="fas fa-map-marker-alt"></i> PIN Code Information</h2>'
    + cost_banner() +
    '<form class="search-form" onsubmit="searchPincode(event)"><input type="text" class="search-input" id="pincode" placeholder="Enter PIN code (e.g., 400001)" pattern="[0-9]{6}" required><button type="submit" class="search-btn">Search</button></form>'
    '</div><div id="results"></div>'
    '<script>'
    'async function searchPincode(e){ e.preventDefault(); const pincode=document.getElementById("pincode").value; const resultsDiv=document.getElementById("results"); resultsDiv.innerHTML = \'<div class="loading"><div class="loading-spinner"></div><p>Fetching location details...</p></div>\';'
    'try{ const response=await fetch("/api/pincode/"+pincode); const data=await response.json();'
    ' if(response.ok && data.d){ let html = \'<div class="results-container">\';'
    ' if(data.d.PostOffice && data.d.PostOffice.length > 0) {'
    '   html += \'<h3 style="margin-bottom:10px;">Location Details</h3>\';'
    '   html += \'<div style="color: var(--success-green); margin-bottom:20px;">\' + (data.d.Message || "Found " + data.d.PostOffice.length + " results") + \'</div>\';'
    '   data.d.PostOffice.forEach((po, idx) => {'
    '     html += \'<div style="margin: 20px 0; padding: 20px; border:1px solid rgba(220,38,38,0.2); border-radius:12px; background:rgba(10,10,10,0.4);">\';'
    '     html += \'<div style="font-weight:700; color:var(--primary-red); margin-bottom:15px;">Result \' + (idx+1) + \': \' + escapeHtml(po.Name || "Post Office") + \'</div>\';'
    '     html += \'<div class="data-grid">\''
    '     + createDataCard("Name", po.Name || "-")'
    '     + createDataCard("PIN Code", po.Pincode || pincode)'
    '     + createDataCard("Branch Type", po.BranchType || "-")'
    '     + createDataCard("Delivery Status", po.DeliveryStatus || "-")'
    '     + createDataCard("Circle", po.Circle || "-")'
    '     + createDataCard("District", po.District || "-")'
    '     + createDataCard("Division", po.Division || "-")'
    '     + createDataCard("Region", po.Region || "-")'
    '     + createDataCard("Block", po.Block || "-")'
    '     + createDataCard("State", po.State || "-")'
    '     + createDataCard("Country", po.Country || "-")'
    '     + \'</div></div>\';'
    '   });'
    ' } else {'
    '   html += \'<div style="color: var(--warning-yellow);">No detailed post office data found</div>\';'
    ' }'
    ' html += \'</div>\'; resultsDiv.innerHTML = html;'
    ' } else { resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-exclamation-circle"></i> Invalid PIN code or no data found</div>\'; }'
    '} catch(err){ console.error(err); resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-times-circle"></i> Error occurred while searching</div>\'; } }'
    '</script>'
    )
    return get_base_template('PIN Code Info - OSINT Tool', content, False)

@app.route('/ip-info')
@login_required
def ip_info():
    if not check_credits(session['username']):
        return redirect(url_for('pricing'))
    content = (
    '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
    '<div class="search-container">'
    '<h2 style="color: var(--primary-red); text-align: center; margin-bottom: 10px;"><i class="fas fa-globe"></i> IP Address Information</h2>'
    + cost_banner() +
    '<form class="search-form" onsubmit="searchIP(event)"><input type="text" class="search-input" id="ipAddress" placeholder="Enter IP address (e.g., 8.8.8.8)" required><button type="submit" class="search-btn">Search</button></form>'
    '</div><div id="results"></div>'
    '<script>'
    'async function searchIP(e){ e.preventDefault(); const ip=document.getElementById("ipAddress").value; const resultsDiv=document.getElementById("results"); resultsDiv.innerHTML = \'<div class="loading"><div class="loading-spinner"></div><p>Looking up IP address...</p></div>\';'
    'try{ const response=await fetch("/api/ip/"+ip); const data=await response.json();'
    ' if(response.ok && data.d){ const info=filterData(data.d); let html=\'<div class="results-container"><h3 style="margin-bottom:20px;">IP Address Details</h3>\';'
    ' html+=\'<div class="data-grid">\''
    ' + createDataCard("IP Address", info.ip || info.query || ip)'
    ' + createDataCard("City", info.city || "-")'
    ' + createDataCard("State/Region", info.state_prov || info.region || info.regionName || "-")'
    ' + createDataCard("Country", info.country_name || info.country || "-")'
    ' + createDataCard("Country Code", info.country_code2 || info.countryCode || "-")'
    ' + createDataCard("ISP", info.isp || "-")'
    ' + createDataCard("Organization", info.organization || info.org || "-")'
    ' + createDataCard("Latitude", info.latitude || info.lat || "-")'
    ' + createDataCard("Longitude", info.longitude || info.lon || "-")'
    ' + createDataCard("Timezone", info.time_zone?.name || info.timezone || "-")'
    ' + createDataCard("Currency", info.currency?.code || "-")'
    ' + createDataCard("Calling Code", info.calling_code || "-")'
    ' + \'</div>\';'
    ' if(info.time_zone) {'
    '   html += \'<div style="margin-top:20px; padding:15px; background:rgba(10,10,10,0.5); border-radius:12px;">\';'
    '   html += \'<h4 style="color:var(--info-blue); margin-bottom:10px;">Timezone Information</h4>\';'
    '   html += \'<div class="data-grid">\''
    '   + createDataCard("Timezone", info.time_zone.name || "-")'
    '   + createDataCard("Current Time", info.time_zone.current_time || "-")'
    '   + createDataCard("Offset", info.time_zone.offset || "-")'
    '   + createDataCard("DST", info.time_zone.is_dst ? "Active" : "Inactive")'
    '   + \'</div></div>\';'
    ' }'
    ' html += \'<div style="margin-top:30px;"><h4 style="color: var(--primary-red); margin-bottom:15px;">Complete Information</h4>\' + renderObject(info) + \'</div></div>\';'
    ' resultsDiv.innerHTML = html; } else { resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-exclamation-circle"></i> Invalid IP address or no data found</div>\'; }'
    '} catch(err){ resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-times-circle"></i> Error occurred while searching</div>\'; } }'
    '</script>'
    )
    return get_base_template('IP Information - OSINT Tool', content, False)

@app.route('/phone-info')
@login_required
def phone_info():
    if not check_credits(session['username']):
        return redirect(url_for('pricing'))
    content = (
    '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
    '<div class="search-container">'
    '<h2 style="color: var(--primary-red); text-align: center; margin-bottom: 10px;"><i class="fas fa-phone"></i> Phone Number Information</h2>'
    + cost_banner() +
    '<form class="search-form" onsubmit="searchPhone(event)"><input type="text" class="search-input" id="phoneNumber" placeholder="Enter phone number" pattern="[0-9]{10}" required><button type="submit" class="search-btn">Search</button></form>'
    '</div><div id="results"></div>'
    '<script>'
    'async function searchPhone(e){ e.preventDefault(); const phone=document.getElementById("phoneNumber").value; const resultsDiv=document.getElementById("results"); resultsDiv.innerHTML = \'<div class="loading"><div class="loading-spinner"></div><p>Searching phone records...</p></div>\';'
    'try{ const response=await fetch("/api/phone/"+phone); const data=await response.json();'
    ' if(response.ok && data.d){ let html = \'<div class="results-container"><h3>Phone Information</h3>\';'
    ' if(Array.isArray(data.d) && data.d.length > 0){'
    '   html += \'<div style="color: var(--success-green); margin: 20px 0;">Found \' + data.d.length + \' record(s)</div>\';'
    '   data.d.forEach((result, idx)=>{'
    '     html += \'<div style="margin: 20px 0; padding: 20px; border:1px solid rgba(220,38,38,0.2); border-radius:12px; background:rgba(10,10,10,0.4);">\';'
    '     html += \'<div style="font-weight:700; color:var(--primary-red); margin-bottom:15px;">Record \' + (idx+1) + \'</div>\';'
    '     html += \'<div class="data-grid">\''
    '     + createDataCard("Name", result.name || "-")'
    '     + createDataCard("Mobile", result.mobile || phone)'
    '     + createDataCard("Father Name", result.father_name || "-")'
    '     + createDataCard("Address", result.address || "-")'
    '     + createDataCard("Alt Mobile", result.alt_mobile || "-")'
    '     + createDataCard("Circle", result.circle || "-")'
    '     + createDataCard("Email", result.email || "-")'
    '     + createDataCard("ID Number", result.id_number || "-")'
    '     + \'</div></div>\';'
    '   });'
    ' } else {'
    '   html += \'<div style="color: var(--warning-yellow); margin-top:20px;">No records found for this number</div>\';'
    ' }'
    ' html += \'</div>\'; resultsDiv.innerHTML = html;'
    ' } else { resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-exclamation-circle"></i> No data found for this phone number</div>\'; }'
    '} catch(err){ console.error(err); resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-times-circle"></i> Error occurred while searching</div>\'; } }'
    '</script>'
    )
    return get_base_template('Phone Lookup - OSINT Tool', content, False)

@app.route('/freefire-info')
@login_required
def freefire_info():
    if not check_credits(session['username']):
        return redirect(url_for('pricing'))
    content = (
    '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
    '<div class="search-container">'
    '<h2 style="color: var(--primary-red); text-align: center; margin-bottom: 10px;"><i class="fas fa-gamepad"></i> Free Fire Player Information</h2>'
    + cost_banner() +
    '<form class="search-form" onsubmit="searchFreeFire(event)"><input type="text" class="search-input" id="playerId" placeholder="Enter Free Fire UID" required><button type="submit" class="search-btn">Search</button></form>'
    '</div><div id="results"></div>'
    '<script>'
    'async function searchFreeFire(e){ e.preventDefault(); const uid=document.getElementById("playerId").value; const resultsDiv=document.getElementById("results"); resultsDiv.innerHTML = \'<div class="loading"><div class="loading-spinner"></div><p>Fetching player stats...</p></div>\';'
    'try{ const response=await fetch("/api/freefire/"+uid); const data=await response.json();'
    ' if(response.ok && data.d && data.d.basicInfo){ const info=filterData(data.d.basicInfo); const social=filterData(data.d.socialInfo || {}); const pet=filterData(data.d.petInfo || {}); const clan=filterData(data.d.clanBasicInfo || {});'
    ' const initials=(info.nickname||"FF").toString().trim().slice(0,2).toUpperCase();'
    ' let html=\'<div class="results-container"><h3 style="margin-bottom:20px;">Player Profile</h3>\';'
    ' html+=\'<div style="display:flex; align-items:center; gap:20px; margin-bottom:30px; padding:20px; background:rgba(10,10,10,0.5); border-radius:15px;">\';'
    ' html+=\'<div style="width:80px; height:80px; border-radius:50%; background:linear-gradient(135deg, var(--primary-red), var(--purple-accent)); display:flex; align-items:center; justify-content:center; font-weight:800; color:white; font-size:1.8rem;">\' + escapeHtml(initials) + \'</div>\';'
    ' html+=\'<div style="flex:1;"><div style="font-size:1.5rem; font-weight:700; color:white;">\' + escapeHtml(info.nickname || "Unknown") + \'</div>\';'
    ' html+=\'<div style="color:var(--text-gray); margin-top:5px;">UID: \' + escapeHtml(info.accountId || uid) + \' • Level \' + escapeHtml(info.level || "-") + \' • Region: \' + escapeHtml(info.region || "-") + \'</div></div></div>\';'
    ' html+=\'<div class="data-grid">\''
    ' + createDataCard("Level", info.level || "-")'
    ' + createDataCard("Experience", info.exp || "-")'
    ' + createDataCard("BR Rank", info.rank || "-")'
    ' + createDataCard("BR Max Rank", info.maxRank || "-")'
    ' + createDataCard("BR Points", info.rankingPoints || "-")'
    ' + createDataCard("CS Rank", info.csRank || "-")'
    ' + createDataCard("CS Max Rank", info.csMaxRank || "-")'
    ' + createDataCard("CS Points", info.csRankingPoints || "-")'
    ' + createDataCard("Badges", info.badgeCnt || "0")'
    ' + createDataCard("Likes", info.liked || "0")'
    ' + createDataCard("Created", info.createAt ? new Date(info.createAt*1000).toLocaleDateString() : "-")'
    ' + createDataCard("Last Login", info.lastLoginAt ? new Date(info.lastLoginAt*1000).toLocaleDateString() : "-")'
    ' + \'</div>\';'
    ' if(clan && clan.clanName){'
    '   html+=\'<div style="margin-top:20px; padding:15px; background:rgba(10,10,10,0.5); border-radius:12px;">\';'
    '   html+=\'<h4 style="color:var(--purple-accent); margin-bottom:10px;">Clan Information</h4>\';'
    '   html+=\'<div class="data-grid">\''
    '   + createDataCard("Clan Name", clan.clanName || "-")'
    '   + createDataCard("Clan Level", clan.clanLevel || "-")'
    '   + createDataCard("Members", clan.memberNum + "/" + clan.capacity || "-")'
    '   + \'</div></div>\';'
    ' }'
    ' if(social && social.signature){'
    '   html+=\'<div style="margin-top:20px; padding:15px; background:rgba(10,10,10,0.5); border-radius:12px;">\';'
    '   html+=\'<h4 style="color:var(--info-blue); margin-bottom:10px;">Social Info</h4>\';'
    '   html+=\'<p style="color:var(--text-light);">Signature: \' + escapeHtml(social.signature || "-") + \'</p>\';'
    '   html+=\'</div>\';'
    ' }'
    ' html += \'</div>\'; resultsDiv.innerHTML = html;'
    ' } else { resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-exclamation-circle"></i> Player not found or invalid UID</div>\'; }'
    '} catch(err){ console.error(err); resultsDiv.innerHTML = \'<div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 10px; color: var(--primary-red);"><i class="fas fa-times-circle"></i> Error occurred while searching</div>\'; } }'
    '</script>'
    )
    return get_base_template('FreeFire Stats - OSINT Tool', content, False)

# Continue with the rest of your routes...
@app.route('/profile')
@login_required
def profile():
    user = users_db[session['username']]
    search_count = len([log for log in search_logs_db if log['username'] == session['username']])
    content = (
        '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 40px; border-radius: 20px; border: 1px solid rgba(220, 38, 38, 0.2);">'
        '<h2 style="color: var(--primary-red); text-align: center; margin-bottom: 30px;">User Profile</h2>'
        '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">'
            '<div style="background: rgba(10, 10, 10, 0.5); padding: 20px; border-radius: 10px; text-align: center;"><div style="font-size: 2rem; color: var(--primary-red); font-weight: 700;">' + session['username'] + '</div><div style="color: var(--text-gray); margin-top: 10px;">Username</div></div>'
            '<div style="background: rgba(10, 10, 10, 0.5); padding: 20px; border-radius: 10px; text-align: center;"><div style="font-size: 2rem; color: var(--success-green); font-weight: 700;">' + str(user.get('credits', 0)) + '</div><div style="color: var(--text-gray); margin-top: 10px;">Credits</div></div>'
            '<div style="background: rgba(10, 10, 10, 0.5); padding: 20px; border-radius: 10px; text-align: center;"><div style="font-size: 2rem; color: var(--info-blue); font-weight: 700;">' + str(search_count) + '</div><div style="color: var(--text-gray); margin-top: 10px;">Searches</div></div>'
        '</div>'
        '<div style="text-align: center; margin: 40px 0;"><p style="color: var(--text-gray);">Your User ID</p><div style="background: rgba(220, 38, 38, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0; font-family: monospace; color: var(--primary-red);">' + user['id'] + '</div></div>'
        '<div style="background: rgba(10, 10, 10, 0.5); padding: 30px; border-radius: 15px;"><h3 style="color: var(--primary-red); margin-bottom: 20px;">Redeem Key</h3>'
        '<form id="redeemForm" style="display: flex; gap: 15px;"><input type="text" id="keyCode" placeholder="Enter key (OSIT-XXXX-XXXX)" style="flex: 1; padding: 14px; background: rgba(10, 10, 10, 0.8); border: 1px solid rgba(220, 38, 38, 0.2); border-radius: 10px; color: white;"><button type="submit" class="btn">Redeem</button></form>'
        '<div id="redeemMessage"></div></div></div>'
        '<script>'
        "document.getElementById('redeemForm').addEventListener('submit', async function(e){ e.preventDefault(); const key=document.getElementById('keyCode').value; const response=await fetch('/api/redeem-key', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({key})}); const data=await response.json(); const msgDiv=document.getElementById('redeemMessage'); if(data.success){ msgDiv.innerHTML='<div style=\"color: var(--success-green); margin-top: 15px;\">Key redeemed! '+data.credits+' credits added.</div>'; setTimeout(()=>location.reload(), 1200);} else { msgDiv.innerHTML='<div style=\"color: var(--primary-red); margin-top: 15px;\">'+(data.error||'Invalid key')+'</div>'; } });"
        '</script>'
    )
    return get_base_template('Profile - OSINT Tool', content, False)

@app.route('/pricing')
@login_required
def pricing():
    contact_link = 'https://t.me/BaignX'
    content = (
    '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
    '<div class="header"><h1>Pricing Plans</h1><p style="color: var(--text-gray);">Contact <a href="' + contact_link + '" target="_blank" style="color: var(--primary-red); text-decoration: underline;">@BaignX</a> to purchase credits.</p></div>'
    '<div class="pricing-grid">'
        '<div class="pricing-card"><h3 style="color: var(--primary-red); font-size: 1.5rem;">Starter</h3><div style="font-size: 3rem; color: var(--primary-red); margin: 20px 0;">$5</div><div style="font-size: 1.5rem; color: var(--success-green);">50 Credits</div><ul style="list-style: none; padding: 20px 0; color: var(--text-gray);"><li style="margin: 10px 0;">✓ 25 searches</li><li style="margin: 10px 0;">✓ Valid 30 days</li><li style="margin: 10px 0;">✓ Basic support</li></ul><a class="btn" href="' + contact_link + '" target="_blank" style="width: 100%; display:block; text-align:center;">Contact @BaignX</a></div>'
        '<div class="pricing-card featured"><h3 style="color: var(--primary-red); font-size: 1.5rem;">Basic</h3><div style="font-size: 3rem; color: var(--primary-red); margin: 20px 0;">$10</div><div style="font-size: 1.5rem; color: var(--success-green);">120 Credits</div><ul style="list-style: none; padding: 20px 0; color: var(--text-gray);"><li style="margin: 10px 0;">✓ 60 searches</li><li style="margin: 10px 0;">✓ Valid 30 days</li><li style="margin: 10px 0;">✓ Priority support</li></ul><a class="btn" href="' + contact_link + '" target="_blank" style="width: 100%; display:block; text-align:center;">Contact @BaignX</a></div>'
        '<div class="pricing-card"><h3 style="color: var(--primary-red); font-size: 1.5rem;">Pro</h3><div style="font-size: 3rem; color: var(--primary-red); margin: 20px 0;">$20</div><div style="font-size: 1.5rem; color: var(--success-green);">300 Credits</div><ul style="list-style: none; padding: 20px 0; color: var(--text-gray);"><li style="margin: 10px 0;">✓ 150 searches</li><li style="margin: 10px 0;">✓ Valid 90 days</li><li style="margin: 10px 0;">✓ Premium support</li></ul><a class="btn" href="' + contact_link + '" target="_blank" style="width: 100%; display:block; text-align:center;">Contact @BaignX</a></div>'
    '</div>'
    )
    return get_base_template('Pricing - OSINT Tool', content, False)

@app.route('/tickets')
@login_required
def tickets():
    user_tickets = []
    for tid, ticket in tickets_db.items():
        if ticket['user_id'] == users_db[session['username']]['id']:
            ticket['id'] = tid
            user_tickets.append(ticket)
    tickets_html = ''
    for ticket in user_tickets:
        tickets_html += (
            '<div class="ticket-card" onclick="window.location.href=\'/ticket/' + ticket['id'] + '\'">'
            '<div style="display: flex; justify-content: space-between; margin-bottom: 10px;">'
            '<span style="color: var(--primary-red);">#' + ticket['id'][:8] + '</span>'
            '<span style="color: var(--text-gray);">' + ticket['status'] + '</span>'
            '</div>'
            '<h3 style="color: white; margin-bottom: 10px;">' + ticket['subject'] + '</h3>'
            '<p style="color: var(--text-gray);">' + (ticket['message'][:100] + '...') + '</p>'
            '</div>'
        )
    if not tickets_html:
        tickets_html = '<div style="text-align: center; color: var(--text-gray); padding: 40px;">No tickets found</div>'
    content = (
        '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
        '<div class="header"><h1>Support Tickets</h1><button class="btn" onclick="showCreateTicket()">Create Ticket</button></div>'
        '<div id="ticketsList">' + tickets_html + '</div>'
        '<div id="createTicketModal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 9999; align-items: center; justify-content: center;">'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.98), rgba(26, 26, 26, 0.95)); padding: 30px; border-radius: 20px; max-width: 500px; width: 90%;">'
        '<h2 style="color: var(--primary-red); margin-bottom: 20px;">Create Ticket</h2>'
        '<form id="ticketForm">'
        '<div class="form-group"><label>Subject</label><input type="text" id="subject" required></div>'
        '<div class="form-group"><label>Message</label><textarea id="message" rows="5" required></textarea></div>'
        '<div style="display: flex; gap: 10px;"><button type="submit" class="btn">Submit</button>'
        '<button type="button" class="btn btn-alt" onclick="hideCreateTicket()">Cancel</button></div>'
        '</form></div></div>'
        '<script>'
        'function showCreateTicket(){ document.getElementById("createTicketModal").style.display = "flex"; }'
        'function hideCreateTicket(){ document.getElementById("createTicketModal").style.display = "none"; }'
        'document.getElementById("ticketForm").addEventListener("submit", async function(e){ e.preventDefault(); const response=await fetch("/api/create-ticket",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ subject: document.getElementById("subject").value, message: document.getElementById("message").value })}); const data=await response.json(); if(data.success){ alert("Ticket created successfully!"); location.reload(); } });'
        '</script>'
    )
    return get_base_template('Support Tickets - OSINT Tool', content, False)

@app.route('/ticket/<ticket_id>')
@login_required
def view_ticket(ticket_id):
    if ticket_id not in tickets_db:
        return redirect('/tickets')
    ticket = tickets_db[ticket_id]
    user = users_db[session['username']]
    if ticket['user_id'] != user['id'] and user.get('role') != 'admin':
        return redirect('/tickets')
    replies_html = ''
    for reply in ticket_replies_db.get(ticket_id, []):
        replies_html += (
            '<div style="background: rgba(10, 10, 10, 0.5); padding: 20px; border-radius: 10px; margin-bottom: 15px;">'
            '<div style="display: flex; justify-content: space-between; margin-bottom: 10px;">'
            '<span style="color: ' + ('var(--primary-red)' if reply.get('is_admin') else 'white') + ';">' + reply['username'] + (' (Admin)' if reply.get('is_admin') else '') + '</span>'
            '<span style="color: var(--text-gray); font-size: 0.9rem;">' + reply.get('created_at', '') + '</span>'
            '</div><p style="color: var(--text-light);">' + reply['message'] + '</p></div>'
        )
    reply_form_html = (
        '<form id="replyForm"><div class="form-group"><label>Add Reply</label><textarea id="replyMessage" rows="3" required></textarea></div><button type="submit" class="btn">Send Reply</button></form>'
        if ticket['status'] != 'CLOSED' else '<div style="text-align: center; color: var(--text-gray);">This ticket is closed</div>'
    )
    content = (
        '<a href="/tickets" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 40px; border-radius: 20px;">'
        '<div style="display: flex; justify-content: space-between; margin-bottom: 20px;"><h2 style="color: var(--primary-red);">Ticket #' + ticket_id[:8] + '</h2><span style="color: var(--text-gray);">' + ticket['status'] + '</span></div>'
        '<h3 style="color: white; margin-bottom: 20px;">' + ticket['subject'] + '</h3>'
        '<div style="background: rgba(10, 10, 10, 0.5); padding: 20px; border-radius: 10px; margin-bottom: 30px;"><p style="color: var(--text-light);">' + ticket['message'] + '</p></div>'
        + replies_html + reply_form_html + '</div>'
        '<script>'
        'const replyForm=document.getElementById("replyForm"); if(replyForm){ replyForm.addEventListener("submit", async function(e){ e.preventDefault(); const response=await fetch("/api/reply-ticket",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ ticket_id: "' + ticket_id + '", message: document.getElementById("replyMessage").value })}); const r=await response.json(); if(r.success){ location.reload(); } }); }'
        '</script>'
    )
    return get_base_template('Ticket #' + ticket_id[:8] + ' - OSINT Tool', content, False)

@app.route('/admin')
@admin_required
def admin():
    total_credits = sum(user.get('credits', 0) for user in users_db.values())
    active_users = sum(1 for user in users_db.values() if user.get('status') == 'active')
    users_table = ''
    for username, user in users_db.items():
        if username != session['username']:
            users_table += (
                '<tr>'
                '<td style="font-family: monospace; font-size: 0.8rem;">' + user['id'][:8] + '...</td>'
                '<td>' + username + '</td>'
                '<td>' + user.get('email', '') + '</td>'
                '<td>' + str(user.get('credits', 0)) + '</td>'
                '<td>' + (user.get('credits_expiry', 'Never')[:10] if user.get('credits_expiry') else 'Never') + '</td>'
                '<td><span class="status-badge status-' + user.get('status', 'active') + '">' + user.get('status', 'active') + '</span></td>'
                '<td>'
                '<button class="btn" data-u="' + username + '" onclick="addCredits(this.dataset.u)" style="padding: 5px 10px; font-size: 0.8rem;">Add</button> '
                '<button class="btn" data-u="' + username + '" onclick="removeCredits(this.dataset.u)" style="padding: 5px 10px; font-size: 0.8rem; background: var(--primary-red);">Remove</button> '
                '<button class="btn btn-alt" data-u="' + username + '" onclick="toggleStatus(this.dataset.u)" style="padding: 5px 10px; font-size: 0.8rem;">' + ('Ban' if user.get('status','active')=='active' else 'Unban') + '</button>'
                '</td></tr>'
            )
    content = (
        '<a href="/dashboard" class="btn" style="display: inline-flex; align-items: center; margin-bottom: 20px;"><i class="fas fa-arrow-left" style="margin-right: 10px;"></i> Back</a>'
        '<div class="header"><h1>Admin Panel</h1><div style="color:var(--text-gray);">Manage users, keys, and settings</div></div>'
        '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px;">'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 25px; border-radius: 15px; text-align: center;"><div style="font-size: 2.2rem; color: var(--primary-red);">' + str(len(users_db)) + '</div><div style="color: var(--text-gray);">Total Users</div></div>'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 25px; border-radius: 15px; text-align: center;"><div style="font-size: 2.2rem; color: var(--success-green);">' + str(total_credits) + '</div><div style="color: var(--text-gray);">Total Credits</div></div>'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 25px; border-radius: 15px; text-align: center;"><div style="font-size: 2.2rem; color: var(--info-blue);">' + str(len(search_logs_db)) + '</div><div style="color: var(--text-gray);">Total Searches</div></div>'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 25px; border-radius: 15px; text-align: center;"><div style="font-size: 2.2rem; color: var(--purple-accent);">' + str(active_users) + '</div><div style="color: var(--text-gray);">Active Users</div></div>'
        '</div>'
        '<div style="display:grid; grid-template-columns: 1.2fr .8fr; gap:20px; margin-bottom:30px;">'
        '<div style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(26, 26, 26, 0.8)); padding: 30px; border-radius: 20px;">'
        '<h2 style="color: var(--primary-red); margin-bottom: 20px;">Users Management</h2>'
        '<div class="admin-users-table"><table><thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Credits</th><th>Expiry</th><th>Status</th><th>Actions</th></tr></thead><tbody>'
        + users_table + '</tbody></table></div></div>'
        '<div style="display:grid; gap:20px;">'
        '<div style="background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); padding: 20px; border-radius: 20px;">'
        '<h2 style="color: var(--primary-red); margin-bottom: 10px;">Settings</h2>'
        '<div class="form-group"><label>Per Search Cost (credits)</label><input type="number" id="searchCostInput" value="' + str(CONFIG['search_cost']) + '" min="1"></div>'
        '<button class="btn" onclick="saveConfig()">Save Settings</button>'
        '</div>'
        '<div style="background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(26,26,26,0.8)); padding: 20px; border-radius: 20px;">'
        '<h2 style="color: var(--primary-red); margin-bottom: 10px;">Generate Key</h2>'
        '<form id="keyForm" style="display: flex; gap: 10px; flex-wrap:wrap;">'
        '<input type="number" id="keyCredits" placeholder="Credits" required style="flex:1; padding: 14px; background: rgba(10, 10, 10, 0.8); border: 1px solid rgba(220, 38, 38, 0.2); border-radius: 10px; color: white;">'
        '<input type="number" id="keyDays" placeholder="Valid days (0=forever)" style="flex:1; padding: 14px; background: rgba(10, 10, 10, 0.8); border: 1px solid rgba(220, 38, 38, 0.2); border-radius: 10px; color: white;">'
        '<button type="submit" class="btn">Generate</button></form>'
        '<div id="generatedKey" style="margin-top: 12px;"></div>'
        '</div></div></div>'
        '<script>'
        'function addCredits(username){ const amount=prompt("Credits to add:"); if(amount){ fetch("/api/admin/modify-credits",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({username, action:"add", amount: parseInt(amount)})}).then(()=>location.reload()); } }'
        'function removeCredits(username){ const amount=prompt("Credits to remove:"); if(amount){ fetch("/api/admin/modify-credits",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({username, action:"remove", amount: parseInt(amount)})}).then(()=>location.reload()); } }'
        'function toggleStatus(username){ fetch("/api/admin/toggle-status",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({username})}).then(()=>location.reload()); }'
        'function saveConfig(){ const v=parseInt(document.getElementById("searchCostInput").value||"0"); if(v>0){ fetch("/api/admin/config",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({search_cost: v})}).then(()=>location.reload()); } else { alert("Enter a valid cost"); } }'
        'document.getElementById("keyForm").addEventListener("submit", async function(e){ e.preventDefault(); const response=await fetch("/api/admin/generate-key",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ credits: parseInt(document.getElementById("keyCredits").value), days: parseInt(document.getElementById("keyDays").value || 0) })}); const data=await response.json(); if(data.success){ document.getElementById("generatedKey").innerHTML = "<div style=\'background: rgba(34, 197, 94, 0.2); padding: 12px; border-radius: 10px; color: var(--success-green);\'>Key: " + data.key + "</div>"; } });'
        '</script>'
    )
    return get_base_template('Admin Panel - OSINT Tool', content, False)

# Enhanced API Routes with Proper Data Handling
def _cost():
    return CONFIG['search_cost']

def clean_api_response(data):
    """Remove unwanted fields from API response"""
    if isinstance(data, dict):
        unwanted_keys = ['dev', 'channel', '_resolved_region']
        return {k: v for k, v in data.items() if k.lower() not in unwanted_keys}
    return data

@app.route('/api/vehicle/<vehicle_number>')
@login_required
def api_vehicle(vehicle_number):
    if not rate_limit_check(request.remote_addr, 'api'):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    if not check_credits(session['username'], _cost()):
        return jsonify({'error': 'Insufficient credits'}), 403
    try:
        url = "https://glonova.in/vc.php/?ng=" + vehicle_number.upper()
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Parse the text response into a dictionary
            text = response.text
            data = {}
            for line in text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            if data and len(data) > 3:
                deduct_credits(session['username'], _cost())
                add_search_log(session['username'], 'vehicle', vehicle_number, True, _cost())
                return jsonify({'d': clean_api_response(data)})
        add_search_log(session['username'], 'vehicle', vehicle_number, False, 0)
        return jsonify({'error': 'No data found'}), 404
    except Exception as e:
        return jsonify({'error': 'Service error'}), 500

@app.route('/api/ifsc/<ifsc_code>')
@login_required
def api_ifsc(ifsc_code):
    if not rate_limit_check(request.remote_addr, 'api'):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    if not check_credits(session['username'], _cost()):
        return jsonify({'error': 'Insufficient credits'}), 403
    try:
        url = "https://ifsc.razorpay.com/" + ifsc_code.upper()
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            deduct_credits(session['username'], _cost())
            add_search_log(session['username'], 'ifsc', ifsc_code, True, _cost())
            return jsonify({'d': clean_api_response(data)})
        add_search_log(session['username'], 'ifsc', ifsc_code, False, 0)
        return jsonify({'error': 'Invalid IFSC'}), 404
    except Exception:
        return jsonify({'error': 'Service error'}), 500

@app.route('/api/pincode/<pincode>')
@login_required
def api_pincode(pincode):
    if not rate_limit_check(request.remote_addr, 'api'):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    if not check_credits(session['username'], _cost()):
        return jsonify({'error': 'Insufficient credits'}), 403
    try:
        url = "https://pincode-info-j4tnx.vercel.app/pincode=" + pincode
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # The API returns an array with a single object
            if data and isinstance(data, list) and len(data) > 0:
                result = data[0]  # Get the first element
                deduct_credits(session['username'], _cost())
                add_search_log(session['username'], 'pincode', pincode, True, _cost())
                return jsonify({'d': clean_api_response(result)})
        add_search_log(session['username'], 'pincode', pincode, False, 0)
        return jsonify({'error': 'Invalid PIN'}), 404
    except Exception as e:
        return jsonify({'error': 'Service error'}), 500

@app.route('/api/ip/<ip_address>')
@login_required
def api_ip(ip_address):
    if not rate_limit_check(request.remote_addr, 'api'):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    if not check_credits(session['username'], _cost()):
        return jsonify({'error': 'Insufficient credits'}), 403
    try:
        url = "https://ip-info.bjcoderx.workers.dev/?ip=" + ip_address
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            deduct_credits(session['username'], _cost())
            add_search_log(session['username'], 'ip', ip_address, True, _cost())
            return jsonify({'d': clean_api_response(data)})
        add_search_log(session['username'], 'ip', ip_address, False, 0)
        return jsonify({'error': 'Invalid IP'}), 404
    except Exception:
        return jsonify({'error': 'Service error'}), 500

@app.route('/api/phone/<phone_number>')
@login_required
def api_phone(phone_number):
    if not rate_limit_check(request.remote_addr, 'api'):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    if not check_credits(session['username'], _cost()):
        return jsonify({'error': 'Insufficient credits'}), 403
    try:
        url = "http://xploide.site/Api.php?num=" + phone_number
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                deduct_credits(session['username'], _cost())
                add_search_log(session['username'], 'phone', phone_number, True, _cost())
                # Return the array directly
                return jsonify({'d': data})
        add_search_log(session['username'], 'phone', phone_number, False, 0)
        return jsonify({'error': 'No data found'}), 404
    except Exception:
        return jsonify({'error': 'Service error'}), 500

@app.route('/api/freefire/<uid>')
@login_required
def api_freefire(uid):
    if not rate_limit_check(request.remote_addr, 'api'):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    if not check_credits(session['username'], _cost()):
        return jsonify({'error': 'Insufficient credits'}), 403
    try:
        url = "http://raw.thug4ff.com/info?uid=" + uid
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and 'basicInfo' in data:
                deduct_credits(session['username'], _cost())
                add_search_log(session['username'], 'freefire', uid, True, _cost())
                return jsonify({'d': clean_api_response(data)})
        add_search_log(session['username'], 'freefire', uid, False, 0)
        return jsonify({'error': 'Player not found'}), 404
    except Exception:
        return jsonify({'error': 'Service error'}), 500

# Other API Routes
@app.route('/api/redeem-key', methods=['POST'])
@login_required
def api_redeem_key():
    key = request.json.get('key', '').upper()
    if key in keys_db and keys_db[key]['status'] == 'unused':
        credits = keys_db[key]['credits']
        users_db[session['username']]['credits'] += credits
        if keys_db[key].get('expiry_days'):
            users_db[session['username']]['credits_expiry'] = (datetime.now() + timedelta(days=keys_db[key]['expiry_days'])).isoformat()
        keys_db[key]['status'] = 'used'
        keys_db[key]['used_by'] = session['username']
        return jsonify({'success': True, 'credits': credits})
    return jsonify({'error': 'Invalid or used key'}), 400

@app.route('/api/create-ticket', methods=['POST'])
@login_required
def api_create_ticket():
    ticket_id = str(uuid.uuid4())
    tickets_db[ticket_id] = {
        'user_id': users_db[session['username']]['id'],
        'username': session['username'],
        'subject': request.json.get('subject'),
        'message': request.json.get('message'),
        'status': 'OPEN',
        'created_at': datetime.now().isoformat()
    }
    return jsonify({'success': True, 'ticket_id': ticket_id})

@app.route('/api/reply-ticket', methods=['POST'])
@login_required
def api_reply_ticket():
    ticket_id = request.json.get('ticket_id')
    message = request.json.get('message')
    if ticket_id not in tickets_db:
        return jsonify({'error': 'Ticket not found'}), 404
    if ticket_id not in ticket_replies_db:
        ticket_replies_db[ticket_id] = []
    ticket_replies_db[ticket_id].append({
        'username': session['username'],
        'message': message,
        'is_admin': users_db[session['username']].get('role') == 'admin',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    return jsonify({'success': True})

# Admin API Routes
@app.route('/api/admin/modify-credits', methods=['POST'])
@admin_required
def admin_modify_credits():
    username = request.json.get('username')
    action = request.json.get('action')
    amount = int(request.json.get('amount', 0))
    if username in users_db:
        if action == 'add':
            users_db[username]['credits'] += amount
        elif action == 'remove':
            users_db[username]['credits'] = max(0, users_db[username]['credits'] - amount)
        return jsonify({'success': True})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/admin/generate-key', methods=['POST'])
@admin_required
def admin_generate_key():
    credits = int(request.json.get('credits', 0))
    days = int(request.json.get('days', 0))
    if credits <= 0:
        return jsonify({'error': 'Invalid credits'}), 400
    key = generate_key()
    keys_db[key] = {
        'credits': credits,
        'expiry_days': days if days > 0 else None,
        'status': 'unused',
        'created_at': datetime.now().isoformat()
    }
    return jsonify({'success': True, 'key': key})

@app.route('/api/admin/config', methods=['POST'])
@admin_required
def admin_config():
    sc = int(request.json.get('search_cost', CONFIG['search_cost']))
    if sc < 1 or sc > 10000:
        return jsonify({'error': 'Invalid search cost'}), 400
    CONFIG['search_cost'] = sc
    return jsonify({'success': True, 'search_cost': sc})

@app.route('/api/admin/toggle-status', methods=['POST'])
@admin_required
def admin_toggle_status():
    username = request.json.get('username')
    if username in users_db:
        current = users_db[username].get('status', 'active')
        users_db[username]['status'] = 'banned' if current == 'active' else 'active'
        return jsonify({'success': True, 'status': users_db[username]['status']})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/health')
def health():
    return jsonify({'ok': True, 'time': datetime.now().isoformat(), 'search_cost': CONFIG['search_cost']})

@app.errorhandler(404)
def not_found(e):
    return redirect('/')

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)