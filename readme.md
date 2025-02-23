# Network Monitor

A Raspberry Pi-based network monitoring system that continuously monitors specified IP addresses and controls GPIO pins based on network connectivity status. The system provides real-time alerts through GPIO pin activation when network issues are detected.

## Table of Contents

- [Overview](#overview)
- [Technical Architecture](#technical-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Features](#features)
- [Testing](#testing)
- [Deployment](#deployment)
- [Performance Considerations](#performance-considerations)
- [Security](#security)
- [Known Limitations](#known-limitations)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Network Monitor is designed to provide continuous monitoring of network devices within a specified IP range. When network connectivity issues are detected, the system triggers a GPIO pin on the Raspberry Pi, which can be used to activate external alert mechanisms (e.g., LED indicators, buzzers, or relay switches).

Key capabilities:

- Continuous monitoring of specified IP ranges
- Whitelist support for critical devices
- Configurable retry attempts and intervals
- GPIO-based alert system
- Comprehensive logging system
- Graceful shutdown handling

## Technical Architecture

The system is built using Python and follows a modular architecture with clear separation of concerns:

```
├── config_loader.py   # Configuration management
├── config.yml        # Configuration file
├── gpio_controller.py # GPIO pin control
├── logger.py         # Logging system
├── main.py          # Application entry point
├── ping_monitor.py   # Core monitoring logic
└── requirements.txt  # Dependencies
```

### Design Patterns

- Singleton pattern for logger and GPIO controller
- Factory pattern for configuration loading
- Observer pattern for monitoring and notification

### Key Technologies

- Python 3.x
- RPi.GPIO for GPIO control
- ping3 for network connectivity testing
- PyYAML for configuration management
- pydantic for data validation

## Prerequisites

- Raspberry Pi (any model with GPIO pins)
- Python 3.x
- Network connectivity
- Required Python packages (see requirements.txt)
- Appropriate permissions for GPIO access

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repo/network-monitor.git
cd network-monitor
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the application by editing `config.yml`

5. Run the application:

```bash
python main.py
```

## Configuration

The system is configured through `config.yml`. Here are the key configuration options:

```yaml
# Network configuration
ip_range:
  start: "192.168.2.114" # Starting IP of the monitoring range
  end: "192.168.2.115" # Ending IP of the monitoring range
whitelist:
  - "192.168.2.111" # Critical IPs to monitor
passlist:
  - "192.168.2.121" # IPs to ignore

# Ping configuration
retry_attempts: 3 # Number of retry attempts for failed pings
retry_interval: 1 # Seconds between retries
iteration_interval: 3 # Seconds between monitoring cycles

# GPIO configuration
gpio_pin: 17 # GPIO pin number for alerts

# Logging configuration
log_file: "network_monitor.log"
log_level: "INFO"
```

## Features

### Network Monitoring

- Continuous IP range scanning
- Configurable retry mechanism
- Whitelist support for critical devices
- Pass list for ignored devices

### GPIO Control

- Automated GPIO pin management
- Clean shutdown handling
- Status indication through pin state

### Logging System

- Comprehensive logging with file and console output
- Configurable log levels
- Timestamped entries

3. Manual Testing Checklist:

- Verify IP range monitoring
- Test whitelist functionality
- Validate GPIO pin control
- Check logging output
- Test graceful shutdown

## Deployment

1. System Service Setup:

```bash
sudo nano /etc/systemd/system/network-monitor.service
```

2. Service Configuration:

```ini
[Unit]
Description=Network Monitor Service
After=network.target

[Service]
ExecStart=/path/to/venv/bin/python /path/to/main.py
WorkingDirectory=/path/to/project
User=pi
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and Start Service:

```bash
sudo systemctl enable network-monitor
sudo systemctl start network-monitor
```

## Performance Considerations

- Use appropriate ping intervals to avoid network congestion
- Consider IP range size impact on monitoring cycle
- Monitor system resource usage
- Implement caching for frequently accessed IPs
- Optimize GPIO operations

## Security

Current security measures:

- Configurable IP ranges
- Whitelist support
- Logging of all activities

Recommended additional measures:

- Implement authentication for configuration changes
- Add SSL/TLS for any future remote management
- Regular security audits
- Rate limiting for ping operations

## Known Limitations

- Single-threaded monitoring
- No web interface for management
- Limited to IPv4 addresses
- No SNMP support
- Basic GPIO control only

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please ensure:

- Code follows PEP 8
- Documentation is updated
- Tests are added/updated
- Commit messages are descriptive

## Troubleshooting

Common issues and solutions:

1. GPIO Permission Issues:

```bash
sudo usermod -a -G gpio $USER
```

2. Network Access Problems:

```bash
# Check if ping requires sudo
sudo setcap cap_net_raw+ep /path/to/venv/bin/python3
```

3. Log Analysis:

```bash
tail -f network_monitor.log
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

For more information or support, please open an issue on the project repository.
