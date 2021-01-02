#!/usr/bin/python
class FilterModule(object):
    def filters(self):
        return {
            'custom_adv_filter': self.custom_adv_filter,
        }

    def custom_adv_filter(self, input_var):
        output_var = []
        
        for os_loop in input_var:
            if bool(os_loop['json'].get('advisories')):
                for adv_loop in os_loop['json']['advisories']:
                    
                    fixed = []
                    if bool(adv_loop.get('firstFixed')):
                        fixed = adv_loop['firstFixed']
                    else:
                        fixed = adv_loop['platforms'][0]['firstFixes'][0]['name']

                    output_var.append({ 'os': os_loop['item']['os'], 
                                        'id': adv_loop['advisoryId'],
                                        'sir': adv_loop['sir'],
                                        'cvss': float(adv_loop['cvssBaseScore']),
                                        'cve': adv_loop.get('cves', []),
                                        'url': adv_loop['publicationUrl'],
                                        'fixed': fixed
                                        })
        return output_var

