import re
from collections import defaultdict
from datetime import datetime
from django.shortcuts import render
import matplotlib.pyplot as plt
from django.conf import settings
import os

ACCESS_LOG = '/var/log/apache2/access.log'
ERROR_LOG = '/var/log/apache2/error.log'

access_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(GET|POST) (/[^ ]*) HTTP/[^"]*" \d+ \d+ "[^"]*" "([^"]*)"')
error_pattern = re.compile(r'\[(.*?)\] \[([a-zA-Z]+)\] \[client (\d+\.\d+\.\d+\.\d+)\] (.*)')

def parse_logs():
    access_stats = defaultdict(lambda: {'count': 0, 'visits': []})
    errors = []

    with open(ACCESS_LOG, 'r') as f:
        for line in f:
            match = access_pattern.match(line)
            if match:
                ip, timestamp, method, page, browser = match.groups()
                timestamp = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')
                access_stats[page]['count'] += 1
                access_stats[page]['visits'].append({
                    'ip': ip,
                    'timestamp': timestamp,
                    'browser': browser
                })

    with open(ERROR_LOG, 'r') as f:
        for line in f:
            match = error_pattern.match(line)
            if match:
                timestamp, level, ip, message = match.groups()
                timestamp = datetime.strptime(timestamp, '%a %b %d %H:%M:%S.%f %Y')
                errors.append({
                    'timestamp': timestamp,
                    'ip': ip,
                    'level': level,
                    'message': message
                })

    return access_stats, errors

def generate_timeline_diagram(access_stats, errors):
    times, accesses, errors_occurred = [], [], []
    
    for page, data in access_stats.items():
        for visit in data['visits']:
            times.append(visit['timestamp'])
            accesses.append(page)

    for error in errors:
        times.append(error['timestamp'])
        errors_occurred.append(error['message'])
    
    plt.figure(figsize=(10, 6))
    plt.plot(times, accesses, 'bo', label="Access")
    plt.plot(times, errors_occurred, 'ro', label="Error")
    plt.xlabel("Time")
    plt.ylabel("Event")
    plt.legend()
    plt.title("Timeline of Page Accesses and Errors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_path = os.path.join(settings.STATIC_ROOT, 'log_analysis/timeline.png')
    plt.savefig(image_path)
    plt.close()
    return 'log_analysis/timeline.png'

def log_stats_view(request):
    access_stats, errors = parse_logs()
    timeline_image = generate_timeline_diagram(access_stats, errors)
    return render(request, 'log_analysis/stats.html', {
        'access_stats': access_stats,
        'errors': errors,
        'timeline_image': timeline_image
    })
