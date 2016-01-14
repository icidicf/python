#!/router/bin/python
# get all the branch green labels from creg
# sort from latest to oldest

import urllib
import re
creg_url = "http://creg-web.cisco.com/labels.php"

def get_creg_greenlabels(branch):
    try:
        return [
            match.group("label")
            for match in re.finditer(
                "<td [^>]+>"
                + branch
                + "</td><td [^>]+>[^<]+</td><td [^>]+>(?P<label>[A-Z0-9_]+)</td><td [^>]+>(?P=label)</td></tr><tr>",
                urllib.urlopen(creg_url).read(),
                flags=re.MULTILINE)
        ]
    except:
        raise Exception("Cannot query green label from CREG.")


mcp_label = get_creg_greenlabels('mcp_dev')
print mcp_label[0]

