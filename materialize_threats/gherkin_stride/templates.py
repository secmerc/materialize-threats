import string

class Base():
    feature_bare = string.Template(
"""
Feature: $component
"""        
    )
    feature_base = string.Template(
"""
Feature: $component
    $scenario
"""
    )

class Scenarios():
    stride = {
        'spoofing': string.Template(
"""
Scenario: Spoofing
    Given $process causes data to flow from $source in $sourceZone to $destination in $destinationZone
    When $source attempts to impersonate something or someone else related to $process
    Then implement and validate digital identity by ...

# Mitigation details
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x11-V2-Authentication.md
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V3-Session-management.md
# https://owasp.org/www-project-proactive-controls/v3/en/c6-digital-identity
"""
        ),
        'tampering': string.Template(
"""
Scenario: Tampering
    Given $process causes data to flow from less trusted $source in $sourceZone to more trusted $destination in $destinationZone
    When $source modifies or otherwise tampers with data related to $process
    Then treat all input as malcious and handle it safely by ...

# Mitigation details
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x18-V10-Malicious.md
"""        
        ),
        'repudiation': string.Template(
"""
Scenario: Repudiation
    Given $process has spoofing and tampering threats
    When $source claims to not have taken an action related to $process
    Then securely log all actions by ... 

# Mitigation details
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x15-V7-Error-Logging.md
"""        
        ),
        'informationDisclosure': string.Template(
"""
Scenario: Information Disclosure
    Given $process causes data to flow from a more trusted $source in $sourceZone to a less trusted $destination in $destinationZone
    When $source attempts to gain access to information it is not authorized to see related to $process
    Then ensure data is protected everywhere by ...

# Mitigation details
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x14-V6-Cryptography.md
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x16-V8-Data-Protection.md
"""
        ),
        'denialOfService': string.Template(
"""
Scenario: Denial of Service
    Given $process causes data to originate from $source outside of our control in $sourceZone
    When $source attempts to deny or degrade service related to $process
    Then ensure service resources are protected and all errors are handled by ...

# Mitigation details
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x19-V11-BusLogic.md
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x20-V12-Files-Resources.md
"""
        ),
        'elevationOfPrivilege': string.Template(
"""
Scenario: Elevation of Privilege
    Given $process causes data to flow from less trusted $source in $sourceZone to more trusted $destination in $destinationZone
    When $source attempts to gain addition capabilities without authorization related to $process
    Then ensure acces control is enforced by ...

# Mitigation details
# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md
"""        
        )

    }
