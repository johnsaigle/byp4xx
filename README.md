***byp4xx.py***
```
    __                __ __           
   / /_  __  ______  / // / _  ___  __
  / __ \/ / / / __ \/ // /_| |/_/ |/_/
 / /_/ / /_/ / /_/ /__  __/>  <_>  <  
/_.___/\__, / .___/  /_/ /_/|_/_/|_|  
      /____/_/                        
```
Python script for 40X responses bypassing. Methods from #bugbountytips, headers, verb tampering and user agents.

Based on the original script by Lobuhi: https://github.com/lobuhi/byp4xx.git

Seeks the same goals as the original script, with some differences:

- Replacing the use of `curl` with python requests for cross-platform use
- Verbose options to print successful requests and responses
- Use of proxy options with Python to support proxying to Burp without using e.g. proxychains
- Tabs replaced with spaces ;)


**Usage:** Start URL with http or https.
```
python3 byp4xx.py <cURL options> <target>

```
**Example:**
```
python3 byp4xx.py https://www.google.es/test
```
**Features:**
- Multiple HTTP verbs/methods
- Multiple methods mentioned in #bugbountytips
- Multiple headers: Referer, X-Custom-IP-Authorization...
- Test for 2454 UserAgents from SecList

**Tips:**
- You can add proxychains to use with BurpSuite
