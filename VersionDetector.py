#coding=utf-8
from burp import IBurpExtender, IHttpListener
import re
import sys

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Version Detector Pro")
        callbacks.registerHttpListener(self)
        # 修复中文输出编码问题
        print(u"Version Detector Pro 加载成功!".encode('utf-8'))  
        
    def processHttpMessage(self, toolFlag, isRequest, messageInfo):
        if not isRequest:
            response = messageInfo.getResponse()
            analyzed = self._helpers.analyzeResponse(response)
            
            server_header = self._get_header_value(analyzed, "Server")
            via_header = self._get_header_value(analyzed, "Via")
            body = response[analyzed.getBodyOffset():].tostring()
            body_version = self._detect_body_version(body)
            
            comment = []
            # 优化显示格式，添加版本类型标识
            if server_header:
                comment.append("Server:%s" % server_header.encode('utf-8'))
            if via_header:
                clean_via = self._extract_version(via_header).encode('utf-8')
                comment.append("Via:%s" % clean_via)
            if body_version:
                comment.append("Body:%s" % body_version.encode('utf-8'))
                
            if comment:
                messageInfo.setHighlight("orange")  # 橙色高亮标记
                messageInfo.setComment(b"||".join(comment))

    def _extract_version(self, header_value):
        patterns = [
            # 增强Kong版本识别
            r'(kong[/\s]?([\d\.]+))',
            # 新增常见反向代理识别
            r'(squid/([\d\.]+))',
            r'(varnish/([\d\.]+))',
            r'(traefik/([\d\.]+))'
        ]
        for pattern in patterns:
            match = re.search(pattern, header_value, re.IGNORECASE)
            if match:
                return "%s %s" % (match.group(1).replace('/', ' '), match.group(2)) if match.lastindex >1 else match.group(1)
        return header_value

    def _detect_body_version(self, body):
        patterns = [
            # 原有正则优化
            r'(nginx/?[\d\.]+)',  
            r'(apache tomcat/?[\d\.]+)',
            r'(apache/?[\d\.]+)',
            # 新增常见组件正则
            r'(kong/?[\d\.]+)',
            r'(jetty/?[\d\.]+)',
            r'(express/?[\d\.]+)',
            r'(kestrel/?[\d\.]+)',
            r'(werkzeug/?[\d\.]+)',
            r'(iis/?[\d\.]+)',
            r'(jboss/?[\d\.]+)',
            r'(glassfish/?[\d\.]+)',
            r'(php/?[\d\.]+)',
            r'(wordpress/?[\d\.]+)',
            # 新增云服务相关
            r'(aws.?elb/[\d\.]+)',
            r'(cloudfront/[\d\.]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)  # 添加大小写不敏感
            if match:
                return match.group(1).upper()  # 统一转为大写
        return None
    
    def _get_header_value(self, analyzed, header_name):
        for header in analyzed.getHeaders():
            if header.startswith(header_name + ":"):
                return header.split(":", 1)[1].strip()
        return None