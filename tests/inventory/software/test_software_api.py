import json

import pytest
import responses

from tenable.exposure_management.inventory.schema import Field, Properties, QueryMode, PropertyFilter, Operator, SortDirection
from tenable.exposure_management.inventory.software.schema import SoftwareValues


@pytest.fixture
def software_properties_response() -> dict[str, list[dict]]:
    return {"properties": [{"key": "cpe", "readable_name": "Common Platform Enumeration",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "cpe:2.3:o:microsoft:windows_7:-:sp2:*:*:*:*:*:*",
                                                  "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Common Platform Enumeration\n## A software inventory technique\n\nCommon Platform Enumeration (CPE) is a software inventory technique that identifies the software installed on a device. CPE uses a standardized format to identify software, which makes it easier to track and manage software assets.\n\nHere are some key points to understand about CPE:\n- **CPE is a standard format for identifying software**. The CPE format consists of a vendor name, product name, version, and edition. This makes it easy to identify software and track changes over time.\n- **CPE can be used to identify both installed and uninstalled software**. This makes it a valuable tool for software inventory and asset management.\n- **CPE can be used to generate reports on software usage**. This information can be used to make decisions about software licensing and usage.\n\n## Example:\n```\nCPE:2.3:Microsoft:Windows_Server:2012_R2:SP1\n```\n\nThis CPE identifies Microsoft Windows Server 2012 R2 Service Pack 1.\n"},
                           {"key": "publisher", "readable_name": "Publisher (Original)",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "tenable", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Publisher (Original)\n## Organization that develops software\nA software publisher is the organization responsible for creating, distributing, and often supporting a software application. They are the entities that hold the intellectual property rights to the software and determine how it is licensed and used.\n\nHere are some key points to understand about software publishers in the context of the cyber industry:\n\n- **Development**: Publishers are involved in the entire software development lifecycle, from conceptualization and coding to testing and release.\n- **Distribution**: They determine how the software is made available to users, whether through direct downloads, app stores, or physical media.\n- **Licensing**: Publishers establish the terms of use for their software through End User License Agreements (EULAs), which define how the software can be used, copied, and distributed.\n- **Support**: Many publishers offer technical support, updates, and patches to address bugs, security vulnerabilities, and compatibility issues.\n- **Security Implications**: The reputation and security practices of a software publisher are crucial considerations in cybersecurity. Using software from reputable publishers with strong security track records can reduce the risk of vulnerabilities and malware. \n"},
                           {"key": "application", "readable_name": "Application (Original)",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "Google Chrome", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Application (Original)\n## A software program\nAn application, often called \"app,\" is a type of software program designed to perform specific tasks or functions for users or other applications. \n\nHere are some key points to understand about applications in the context of the cyber industry:\n\n- **User-facing applications:** These applications are designed for direct interaction with end-users. Examples include web browsers, email clients, word processors, spreadsheets, and games.\n- **System applications:** These applications interact with the computer system or other applications. Examples include operating systems, device drivers, programming tools, and system utilities.\n- **Web applications:** These applications run on web servers and are accessed by users through web browsers over the internet or intranet. Examples include online shopping websites, social media platforms, and online banking portals.\n- **Mobile applications:** These applications are specifically designed to run on mobile devices such as smartphones and tablets. They can be native apps (developed for a specific platform like iOS or Android) or web-based apps accessed through the device's web browser.\n- **Embedded applications:** These applications are integrated into specific devices or systems to control their functionality. Examples include firmware in routers, control systems in industrial equipment, and software in medical devices. \n"},
                           {"key": "version", "readable_name": "Version",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "154.69.0", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Version\n## The version of a software\n\nThe version of a software is a unique identifier that indicates the specific release of the software. It is typically composed of a major version number, a minor version number, and a build number. For example, the version of Windows 10 is 10.0.19041.867.\n\nThe version of a software can be important for several reasons. First, it can indicate whether the software has been patched with security updates. Second, it can indicate whether the software is compatible with other systems and applications. Third, it can be used to track changes in the software over time.\n\nIn the context of cyber security, the version of a software can be important for several reasons. First, it can be used to identify vulnerabilities in the software. Second, it can be used to determine whether the software is up-to-date with security patches. Third, it can be used to track changes in the software over time.\n"},
                           {"key": "software_update", "readable_name": "Software Update",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "3.0", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Software Update\n## A software update is a set of files that can be installed on a device to update the software on that device.\n\nSoftware updates are typically released by software vendors to fix bugs, add new features, or improve security. They can be installed manually or automatically.\n\nHere are some key points to understand about software updates in the context of the cyber industry:\n- **Importance of Software Updates**: Software updates are important because they can help to keep devices secure and up-to-date. By installing software updates, users can help to protect their devices from vulnerabilities that could be exploited by attackers.\n- **Types of Software Updates**: There are two main types of software updates: security updates and feature updates. Security updates are released to fix vulnerabilities in software. Feature updates are released to add new features or improve existing features.\n- **How to Install Software Updates**: Software updates can be installed manually or automatically. To install a software update manually, users can download the update from the software vendor's website and then install it on their device. To install a software update automatically, users can enable automatic updates in their device's settings.\n"},
                           {"key": "edition", "readable_name": "Edition",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "MacOS High Sierra", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Edition\n## A software version\n\nAn edition is a specific version of a software product. It may include additional features or functionality not found in other editions. Editions are typically named after their features or functionality, such as \"Standard Edition\" or \"Enterprise Edition.\"\n\nHere are some key points to understand about editions in the context of the cyber industry:\n- **Editions are typically named after their features or functionality**. For example, a software product may have a \"Standard Edition\" and an \"Enterprise Edition.\" The Enterprise Edition may include additional features or functionality not found in the Standard Edition.\n- **Editions are often used to differentiate between different levels of support**. For example, a software vendor may offer a higher level of support for customers who purchase the Enterprise Edition of their product.\n- **Editions can also be used to differentiate between different pricing tiers**. For example, a software vendor may charge more for the Enterprise Edition of their product than for the Standard Edition.\n"},
                           {"key": "software_edition", "readable_name": "Software Edition",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "Microsoft Power BI", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Software Edition\n## The version of a software\n\nThe software edition is the version of a software. It can be used to identify the specific features and functionality that are included in the software. For example, the software edition might be \"Enterprise\" or \"Standard.\"\n\nHere are some key points to understand about software editions in the context of the cyber industry:\n- **Software Editions and Security**: Software editions can have a significant impact on security. For example, some editions might include additional security features that are not available in other editions. It is important to select the software edition that meets your security needs.\n- **Software Editions and Compliance**: Software editions can also impact compliance. For example, some regulations might require that you use a specific software edition. It is important to select the software edition that meets your compliance requirements.\n- **Software Editions and Cost**: Software editions can also impact cost. For example, some editions might be more expensive than others. It is important to select the software edition that meets your budget.\n"},
                           {"key": "target_software", "readable_name": "Target Software",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "Enterprise", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Target Software\n## Software properties\n\nTarget Software is a software property that indicates the software that is running on a device. This property can be used to identify the specific software that is installed on a device, as well as the version of the software. This information can be used to assess the risk of a device being vulnerable to attack, as well as to determine the appropriate security measures that should be taken to protect the device.\n\nHere are some key points to understand about Target Software in the context of the cyber industry:\n- **Software Identification**: Target Software can be used to identify the specific software that is installed on a device. This information can be used to assess the risk of a device being vulnerable to attack, as well as to determine the appropriate security measures that should be taken to protect the device.\n- **Software Version**: Target Software can also be used to identify the version of the software that is installed on a device. This information can be used to determine whether the software is up-to-date with the latest security patches. If the software is not up-to-date, it may be vulnerable to attack.\n- **Software Vulnerability**: Target Software can also be used to identify vulnerabilities in the software that is installed on a device. This information can be used to assess the risk of a device being attacked and to determine the appropriate security measures that should be taken to protect the device.\n"},
                           {"key": "target_hardware", "readable_name": "Target Hardware",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "CPU", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Target Hardware\n## The hardware that a software is designed to run on\n\nTarget hardware is the hardware that a software is designed to run on. This can include specific types of processors, operating systems, and other hardware components. It is important to ensure that the target hardware is compatible with the software before installing it.\n\nHere are some key points to understand about target hardware in the context of the cyber industry:\n- **Compatibility**: The target hardware must be compatible with the software in order for it to run properly. This means that the hardware must have the necessary components and be running the correct operating system.\n- **Performance**: The target hardware will affect the performance of the software. For example, a software that is designed to run on a high-end processor will not perform well on a low-end processor.\n- **Security**: The target hardware can also affect the security of the software. For example, a software that is designed to run on a secure operating system will be more secure than a software that is designed to run on an insecure operating system.\n\nIt is important to choose the correct target hardware for the software in order to ensure compatibility, performance, and security.\n"},
                           {"key": "software_language", "readable_name": "Software Language",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "Java", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Software Language\n## The language used to write a software\n\nA software language is a set of rules that define how to write software. It is a way of communicating with a computer. Software languages are used to create programs, scripts, and other types of software.\n\nThere are many different software languages, each with its own strengths and weaknesses. Some popular software languages include Python, Java, C++, and JavaScript.\n\nSoftware languages are constantly evolving, with new languages being created and old languages being updated. This is because the needs of software developers are constantly changing.\n\nSoftware languages are an essential part of the software development process. They allow developers to communicate with computers and create the software that we use every day.\n"},
                           {"key": "software_other", "readable_name": "Software Other",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "Chrome", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Software Other\n## Properties of software\n\nSoftware Other is a category of software that does not fall into any of the other categories. It includes software that is not used for business purposes, such as games, entertainment software, and personal productivity software. It also includes software that is used for business purposes but is not critical to the operation of the organization, such as office productivity software and graphics software.\n\nSoftware Other can be a source of security vulnerabilities. It is important to keep software up to date and to install security patches as soon as they are available. It is also important to have a strong security policy in place that covers the use of Software Other.\n\nHere are some key points to understand about Software Other in the context of the cyber industry:\n- **Types of Software Other**: Software Other can include a wide variety of software, such as games, entertainment software, personal productivity software, office productivity software, and graphics software.\n- **Security Risks**: Software Other can be a source of security vulnerabilities. It is important to keep software up to date and to install security patches as soon as they are available. It is also important to have a strong security policy in place that covers the use of Software Other.\n- **Mitigation Strategies**: Mitigation strategies for Software Other include keeping software up to date, installing security patches, and having a strong security policy in place.\n"},
                           {"key": "display_publisher", "readable_name": "Publisher",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "tenable", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Publisher\n## Organization that develops software\nA software publisher is the organization responsible for creating, distributing, and often supporting a software application. They are the entities that hold the intellectual property rights to the software and determine how it is licensed and used.\n\nHere are some key points to understand about software publishers in the context of the cyber industry:\n\n- **Development**: Publishers are involved in the entire software development lifecycle, from conceptualization and coding to testing and release.\n- **Distribution**: They determine how the software is made available to users, whether through direct downloads, app stores, or physical media.\n- **Licensing**: Publishers establish the terms of use for their software through End User License Agreements (EULAs), which define how the software can be used, copied, and distributed.\n- **Support**: Many publishers offer technical support, updates, and patches to address bugs, security vulnerabilities, and compatibility issues.\n- **Security Implications**: The reputation and security practices of a software publisher are crucial considerations in cybersecurity. Using software from reputable publishers with strong security track records can reduce the risk of vulnerabilities and malware. \n"},
                           {"key": "display_application", "readable_name": "Application",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "tenable", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Application\n## A software program\nAn application, often called \"app,\" is a type of software program designed to perform specific tasks or functions for users or other applications. \n\nHere are some key points to understand about applications in the context of the cyber industry:\n\n- **User-facing applications:** These applications are designed for direct interaction with end-users. Examples include web browsers, email clients, word processors, spreadsheets, and games.\n- **System applications:** These applications interact with the computer system or other applications. Examples include operating systems, device drivers, programming tools, and system utilities.\n- **Web applications:** These applications run on web servers and are accessed by users through web browsers over the internet or intranet. Examples include online shopping websites, social media platforms, and online banking portals.\n- **Mobile applications:** These applications are specifically designed to run on mobile devices such as smartphones and tablets. They can be native apps (developed for a specific platform like iOS or Android) or web-based apps accessed through the device's web browser.\n- **Embedded applications:** These applications are integrated into specific devices or systems to control their functionality. Examples include firmware in routers, control systems in industrial equipment, and software in medical devices. \n"},
                           {"key": "file_location", "readable_name": "File location",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "/opt/nessus_agent", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# File location\n## The location of a file on a device\n\nThe file location is the path to a file on a device. It is typically represented as a series of folders and subfolders, separated by slashes (/). For example, the file location for the file \"index.html\" on the web server \"www.example.com\" would be \"/var/www/html/index.html\".\n\nThe file location is important because it determines where a file is stored on a device and how it can be accessed. For example, a file that is stored in a public location, such as the web server's root directory, can be accessed by anyone who has access to the web server. However, a file that is stored in a private location, such as a user's home directory, can only be accessed by the user who owns it.\n\nThe file location can also be used to determine the file's type and permissions. For example, a file that is stored in the \"/bin\" directory is typically an executable file, while a file that is stored in the \"/etc\" directory is typically a configuration file. The file's permissions can also be determined by its location. For example, a file that is stored in the \"/root\" directory typically has root permissions, while a file that is stored in a user's home directory typically has the user's permissions.\n"},
                           {"key": "port_binding_count", "readable_name": "Port Binding Count",
                            "control": {"type": "NUMBER", "multiple_allowed": False,
                                        "regex": {"hint": "6", "expression": "^\\d+$"}},
                            "operators": ["=", ">=", ">", "<=", "<", "exists", "not exists"], "sortable": True,
                            "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Port Binding Count\n## The number of ports that are bound to a software.\n\nPort binding is a security feature that helps to protect a software application from unauthorized access. When a port is bound to a software application, only that application can use the port. This helps to prevent other applications from accessing the port and potentially compromising the software application.\n\nThe port binding count is a measure of the number of ports that are bound to a software application. A high port binding count indicates that the software application is well-protected from unauthorized access. A low port binding count indicates that the software application may be vulnerable to unauthorized access.\n\nThe port binding count can be used to assess the security of a software application. A high port binding count indicates that the software application is well-protected from unauthorized access. A low port binding count indicates that the software application may be vulnerable to unauthorized access.\n"},
                           {"key": "ports", "readable_name": "Ports",
                            "control": {"type": "NUMBER", "multiple_allowed": True,
                                        "regex": {"hint": "22", "expression": "^\\d+$"}},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0, "object_types": [],
                            "description": "# Ports\n## A network port is a logical construct that identifies a specific network service.\n\nA port is a logical construct that identifies a specific network service. It is a number that is used to identify the application or service that is running on a computer. Ports are used by the TCP/IP protocol to route data to the correct application.\n\nThere are two main types of ports: well-known ports and registered ports. Well-known ports are ports that are used by specific applications. For example, port 80 is used for HTTP, port 22 is used for SSH, and port 443 is used for HTTPS. Registered ports are ports that are assigned to specific applications by the Internet Assigned Numbers Authority (IANA).\n\nPorts can be used to identify both the source and destination of network traffic. For example, if a computer is sending data to port 80 on another computer, then the source port is the port on the sending computer and the destination port is the port on the receiving computer.\n\nPorts can also be used to control access to network services. For example, a firewall can be configured to allow or deny traffic to specific ports. This can be used to block access to certain applications or services.\n\nPorts are an important part of the TCP/IP protocol and are used to route data to the correct application. They can also be used to identify the source and destination of network traffic and to control access to network services.\n"},
                           {"key": "protocols", "readable_name": "Protocols",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "regex": {"hint": "TCP", "expression": ".*"}},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0, "object_types": [],
                            "description": "# Protocols\n## A set of rules that govern the communication between two or more entities\n\nA protocol is a set of rules that govern the communication between two or more entities. It defines the format and timing of messages, as well as the rules for error handling and recovery. Protocols are used in a variety of contexts, including computer networking, telecommunications, and business.\n\nIn the context of cyber security, protocols are used to ensure that communication between devices is secure. For example, the Secure Sockets Layer (SSL) protocol is used to encrypt data that is transmitted over the internet. This helps to protect sensitive information, such as credit card numbers and passwords, from being intercepted by malicious actors.\n\nProtocols are also used to authenticate users and devices. For example, the Kerberos protocol is used to authenticate users on a network. This helps to prevent unauthorized access to resources.\n\nProtocols are an essential part of cyber security. They help to ensure that communication between devices is secure and that users and devices are properly authenticated.\n"},
                           {"key": "last_seen_version", "readable_name": "Last Seen Version",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "1.2.6", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Last Seen Version\n## The last version of the software that was seen on the device\n\nThe last seen version is the most recent version of the software that was detected on the device. This information can be used to identify outdated software that may be vulnerable to attack.\n\nHere are some key points to understand about last seen versions in the context of the cyber industry:\n- **Software Versions**: Software versions are different iterations of the same software. They typically include bug fixes, security updates, and new features.\n- **Outdated Software**: Software that is not up to date with the latest version is considered outdated. Outdated software may be vulnerable to attack and should be patched as soon as possible.\n- **Vulnerabilities**: Vulnerabilities are weaknesses in software that can be exploited by attackers. Outdated software is often more vulnerable to attack than up-to-date software.\n- **Patches**: Patches are updates that fix vulnerabilities in software. They should be installed as soon as possible to reduce the risk of attack.\n\nThe last seen version can be used to identify outdated software that may be vulnerable to attack. This information can be used to prioritize patching efforts and to identify devices that may need to be replaced.\n"},
                           {"key": "eol_date", "readable_name": "Security End Of Life",
                            "control": {"type": "DATE", "multiple_allowed": False,
                                        "regex": {"hint": "timestamp", "expression": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}},
                            "operators": ["=", ">", "<", "between", "exists", "not exists", "older than", "newer than",
                                          "within last"], "sortable": True, "filterable": True, "weight": 0.0,
                            "object_types": [],
                            "description": "# Security End Of Life \n## Software no longer supported by vendor\nSecurity End of Life (EOL) for software refers to the point in time when a software vendor ceases to provide support, updates, and security patches for a particular software product. \n\nHere's what you need to know about Security End of Life:\n\n- **Increased Security Risks:**  Without security updates, software becomes vulnerable to newly discovered threats.\n- **Compliance Violations:** Using EOL software may violate regulatory and industry compliance standards.\n- **Lack of Support:**  Vendors typically don't offer assistance for issues encountered with EOL software.\n- **Compatibility Issues:** EOL software may not be compatible with newer operating systems or hardware.\n- **Data Loss and Downtime:** Exploited vulnerabilities in EOL software can lead to data breaches, system downtime, and operational disruptions. \n"},
                           {"key": "devices_count", "readable_name": "Devices Count",
                            "control": {"type": "NUMBER", "multiple_allowed": False,
                                        "regex": {"hint": "5", "expression": "^\\d+$"}},
                            "operators": ["=", ">=", ">", "<=", "<", "exists", "not exists"], "sortable": True,
                            "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Devices Count\n## The number of devices that have a given property\n\nThe devices count is a metric that measures the number of devices that have a given property. This can be used to track the number of devices that are running a specific software version, have a certain vulnerability, or are located in a particular geographic region.\n\nThe devices count can be used to identify potential security risks. For example, if a large number of devices are running an outdated software version, they may be vulnerable to attack. The devices count can also be used to track the effectiveness of security measures. For example, if the number of devices with a particular vulnerability decreases after a patch is released, this indicates that the patch is effective.\n\nThe devices count is a valuable metric for cyber asset management. It can be used to track the health and security of devices, identify potential risks, and measure the effectiveness of security measures.\n"},
                           {"key": "version_count", "readable_name": "Version Count",
                            "control": {"type": "NUMBER", "multiple_allowed": False,
                                        "regex": {"hint": "5", "expression": "^\\d+$"}},
                            "operators": ["=", ">=", ">", "<=", "<", "exists", "not exists"], "sortable": True,
                            "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Version Count\n## The number of versions of a software\n\nThe version count is the number of different versions of a software that have been released. This can be used to track the maturity of a software and to identify potential security vulnerabilities.\n\nHere are some key points to understand about version count in the context of the cyber industry:\n- **Software Versions**: A software version is a specific release of a software product. It is typically identified by a version number, which is a unique identifier that consists of one or more numbers or letters.\n- **Software Maturity**: The maturity of a software is a measure of its stability and reliability. A software that has been released in multiple versions is generally considered to be more mature than a software that has only been released in a single version.\n- **Security Vulnerabilities**: A security vulnerability is a weakness in a software that can be exploited by an attacker to gain unauthorized access to a system or to steal data. Software that has been released in multiple versions is more likely to have security vulnerabilities than software that has only been released in a single version.\n\nThe version count can be used to track the maturity of a software and to identify potential security vulnerabilities. A software that has been released in multiple versions is generally considered to be more mature than a software that has only been released in a single version. Software that has been released in multiple versions is also more likely to have security vulnerabilities than software that has only been released in a single version.\n"},
                           {"key": "cpe_count", "readable_name": "Cpe Count",
                            "control": {"type": "NUMBER", "multiple_allowed": False,
                                        "regex": {"hint": "5", "expression": "^\\d+$"}},
                            "operators": ["=", ">=", ">", "<=", "<", "exists", "not exists"], "sortable": True,
                            "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Cpe Count\n## The number of CPEs associated with a software\n\nA CPE (Common Platform Enumeration) is a unique identifier for a software product. It is used to track software vulnerabilities and ensure that the correct patches are applied. The CPE Count property indicates the number of CPEs associated with a given software asset. This can be useful for identifying software that is out of date or has known vulnerabilities.\n\nHere are some key points to understand about the CPE Count property:\n- **CPEs are used to track software vulnerabilities**. A CPE is a unique identifier for a software product. It is used to track software vulnerabilities and ensure that the correct patches are applied.\n- **The CPE Count property indicates the number of CPEs associated with a given software asset**. This can be useful for identifying software that is out of date or has known vulnerabilities.\n- **The CPE Count property can be used to generate reports and identify trends**. For example, you could use the CPE Count property to generate a report that shows the number of software assets with known vulnerabilities. You could also use the CPE Count property to identify trends in the number of software assets with known vulnerabilities over time.\n"},
                           {"key": "file_location_count", "readable_name": "File Location Count",
                            "control": {"type": "NUMBER", "multiple_allowed": False,
                                        "regex": {"hint": "5", "expression": "^\\d+$"}},
                            "operators": ["=", ">=", ">", "<=", "<", "exists", "not exists"], "sortable": True,
                            "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# File Location Count\n## The number of unique locations where a file is stored\n\nThe file location count is a property that indicates the number of unique locations where a file is stored. This can be useful for identifying files that are stored in multiple locations, which may be an indication of a security risk.\n\nFor example, if a file is stored in both the user's home directory and the system's temp directory, it may be more difficult to control who has access to the file. Additionally, if a file is stored in multiple locations, it may be more difficult to keep track of changes to the file.\n\nThe file location count can be used to identify files that are stored in multiple locations and to track changes to files. This information can be used to improve security by ensuring that files are only stored in authorized locations and that changes to files are tracked.\n"},
                           {"key": "type", "readable_name": "Type",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "regex": {"hint": "Operating System", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 0.0, "object_types": [],
                            "description": "# Type\n## The type of a software\n\nThe type of a software is a classification that indicates the purpose or function of the software. Common types of software include:\n- **Application Software**: Software that is designed to perform a specific task or set of tasks. Examples include word processing software, spreadsheets, and databases.\n- **System Software**: Software that is designed to manage the operation of a computer system. Examples include operating systems, device drivers, and utilities.\n- **Middleware**: Software that acts as a bridge between application software and system software. Examples include database management systems, application servers, and web servers.\n- **Platform Software**: Software that provides a foundation for the development and execution of other software. Examples include operating systems, virtual machines, and development tools.\n\nThe type of a software can be used to identify potential vulnerabilities and risks. For example, application software is more likely to contain vulnerabilities than system software, because it is more complex and is often developed by third-party vendors.\n"},
                           {"key": "asset_sources", "readable_name": "Sources",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "selection": [{"name": "AWS Connector", "value": "AWS", "deprecated": True},
                                                      {"name": "AWS SSM agent", "value": "SSM", "deprecated": True},
                                                      {"name": "Agent", "value": "NESSUS_AGENT", "deprecated": True},
                                                      {"name": "Azure Connector", "value": "AZURE", "deprecated": True},
                                                      {"name": "Azure Frictionless Assessment", "value": "AZURE_FA",
                                                       "deprecated": True},
                                                      {"name": "GCP Connector", "value": "GCP", "deprecated": True},
                                                      {"name": "Nessus Network Monitor", "value": "PVS",
                                                       "deprecated": True},
                                                      {"name": "Nessus", "value": "NESSUS_SCAN", "deprecated": True},
                                                      {"name": "Tenable Web Application Scanning", "value": "WAS",
                                                       "deprecated": False},
                                                      {"name": "Tenable Identity Exposure", "value": "TIE",
                                                       "deprecated": False},
                                                      {"name": "Tenable Cloud Security (Legacy)", "value": "T.CS",
                                                       "deprecated": True},
                                                      {"name": "Tenable Cloud Security", "value": "CLOUD",
                                                       "deprecated": False},
                                                      {"name": "Tenable Attack Surface Management", "value": "ASM",
                                                       "deprecated": False},
                                                      {"name": "Tenable Vulnerability Management", "value": "T.IO",
                                                       "deprecated": False},
                                                      {"name": "Tenable OT Security", "value": "T.OT",
                                                       "deprecated": False},
                                                      {"name": "Tenable Container Security", "value": "CONSEC",
                                                       "deprecated": False}, {"name": "Tenable Cloud Security (core)",
                                                                              "value": "CORE_CLOUDRESOURCE",
                                                                              "deprecated": True},
                                                      {"name": "Qualys VMDR", "value": "QUALYS", "deprecated": False,
                                                       "third_party": True},
                                                      {"name": "SentinelOne Singularity", "value": "SENTINEL_ONE",
                                                       "deprecated": False, "third_party": True},
                                                      {"name": "Rapid7 InsightVM", "value": "RAPID_7",
                                                       "deprecated": True},
                                                      {"name": "Tenable Security Center", "value": "SECURITY_CENTER",
                                                       "deprecated": False},
                                                      {"name": "Carbon Black Workload", "value": "CARBON_BLACK",
                                                       "deprecated": True},
                                                      {"name": "Microsoft Defender", "value": "MICROSOFT_DEFENDER",
                                                       "deprecated": False, "third_party": True},
                                                      {"name": "CrowdStrike Falcon", "value": "CROWDSTRIKE",
                                                       "deprecated": False},
                                                      {"name": "ServiceNow", "value": "SERVICE_NOW",
                                                       "deprecated": False},
                                                      {"name": "Unclassified", "value": "UNCLASSIFIED",
                                                       "deprecated": False}]},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0, "object_types": [],
                            "description": "# Sources\n## The origin of a software\n\nThe source of a software is the place where it was created or obtained. It can be a software vendor, a repository, or a third-party website. The source of a software is important because it can affect its security and reliability. For example, software obtained from a reputable vendor is more likely to be secure than software obtained from an unknown source.\n\nHere are some key points to understand about sources in the context of the cyber industry:\n- **Software Vendors**: These are companies that develop and sell software. They are the primary source of software for most organizations.\n- **Repositories**: These are online storage locations where software can be downloaded. Repositories can be public or private. Public repositories are open to anyone, while private repositories are only accessible to authorized users.\n- **Third-Party Websites**: These are websites that offer software for download. They can be legitimate or malicious. Legitimate third-party websites offer software from reputable vendors, while malicious third-party websites offer software that is infected with malware.\n\nIt is important to be aware of the source of software before installing it. Software obtained from a reputable source is more likely to be secure and reliable.\n"},
                           {"key": "last_seen", "readable_name": "Last Seen",
                            "control": {"type": "DATE", "multiple_allowed": False,
                                        "regex": {"hint": "timestamp", "expression": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}},
                            "operators": ["=", ">", "<", "between", "exists", "not exists", "older than", "newer than",
                                          "within last"], "sortable": True, "filterable": True, "weight": 0.0,
                            "object_types": [],
                            "description": """# Last Seen\n## The date and time when a software was last seen on a device\n\nLast seen is a property that indicates the date and time when a software was last seen on a device. This information can be used to track the movement of software across devices and to identify devices that may have been compromised.\n\nHere are some key points to understand about last seen in the context of the cyber industry:\n- **Last seen is a valuable indicator of device compromise**. If a software is seen on a device that it is not typically installed on, it may be a sign that the device has been compromised.\n- **Last seen can be used to track the movement of software across devices**. This information can be used to identify devices that may have been compromised or to track the spread of malware.\n- **Last seen can be used to identify devices that are not being used** Connection #0 to host qa-develop.cloud.aws.tenablesecurity.com left intact
                                           *.This information can be used to save money on energy costs or to identify
                           devices that may be vulnerable to attack.\n"""}]}


@pytest.fixture
def software_response() -> dict:
    return {"values": [{"application": ".net_framework", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 2}},
                       {"application": "edge", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}},
                       {"application": "onedrive", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 3}},
                       {"application": "remote_desktop_connection", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}},
                       {"application": "sql_server", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}},
                       {"application": "windows_defender", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}}], "total_count": 6,
            "offset": 0, "limit": 100, "sort_by": "application", "sort_direction": "desc"
            }


@responses.activate
def test_properties_list(api, software_properties_response):
    # Arrange
    responses.get('https://cloud.tenable.com/inventory/api/v1/software/properties',
                  json=software_properties_response,
                  match=[responses.matchers.query_param_matcher({})])
    # Act
    software_properties_result: list[Field] = api.software.list_properties()
    # Assert
    assert software_properties_result == Properties(**software_properties_response).properties


@responses.activate
def test_list(api, software_response):
    query_text = "accurics"
    query_mode = QueryMode.SIMPLE
    filters = [PropertyFilter(property="property", operator=Operator.EQUAL, value=["value"])]

    extra_properties = ["apa_asset_total_paths_count"]
    offset = 0
    limit = 100
    sort_by = "application"
    sort_direction = SortDirection.DESC
    timezone = "America/Chicago"

    # Construct the dictionary using variables
    payload = {
        "search": {
            "query": {
                "text": query_text,
                "mode": query_mode.value
            },
            "filters": [filter.model_dump(mode='json') for filter in filters]
        },
        "extra_properties": extra_properties,
        "offset": offset,
        "limit": limit,
        "sort_by": sort_by,
        "sort_direction": sort_direction.value,
        "timezone": timezone
    }
    responses.add(responses.POST,
                  'https://cloud.tenable.com/inventory/api/v1/software',
                  json=software_response,
                  match=[responses.matchers.body_matcher(params=json.dumps(payload))])
    # Act
    software: SoftwareValues = api.software.list(query_text=query_text, query_mode=query_mode,
                                                 filters=filters, extra_properties=extra_properties,
                                                 offset=offset, limit=limit, sort_by=sort_by,
                                                 sort_direction=sort_direction, timezone=timezone)
    # Assert
    assert software == SoftwareValues(**software_response)
