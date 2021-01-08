#!/usr/bin/python
class FilterModule(object):
    def filters(self):
        return {
            'custom_adv_filter': self.custom_adv_filter,
        }

    def custom_adv_filter(self, input_var):
        output_var = []
        
        for os_loop in input_var:
            print(os_loop['item']['os'])
            if (os_loop['json'].get('advisories')):
                for adv_loop in os_loop['json']['advisories']:
                    
                    # catch two possible data structures with first fixed releases
                    fixed = []
                    if (adv_loop.get('firstFixed')):
                        fixed = adv_loop['firstFixed']
                    else:
                        fixed = adv_loop['platforms'][0]['firstFixes'][0]['name']
                        
                    # catch cvss score string that contains no number
                    try:
                        cvss_float = float(adv_loop['cvssBaseScore'])
                    except ValueError:
                        cvss_float = 0.0

                    output_var.append({ 'os': os_loop['item']['os'], 
                                        'id': adv_loop['advisoryId'],
                                        'sir': adv_loop['sir'],
                                        'cvss': cvss_float),
                                        'cve': adv_loop.get('cves', []),
                                        'url': adv_loop['publicationUrl'],
                                        'fixed': fixed
                                        })
        return output_var

