import re

s = 'Intel Celeron N2930 @ 1.83GHz'
s = 'Intel Xeon E3-1275 v6 @ 3.80GHz'
s = '​Intel Core i7-11850H @ 2.50GHz'
# s = 'Intel Celeron 3.06GHz'
s = 'ARM Cortex-A17 4 Core 1800 MHz'
def _get_cpu_name_and_ghz(self, s):
        ghz = None
        last = None
        if s:
            s = s.strip()
            p = '@* *([\d\.\s]+(?:ghz|mhz))$'
            res = re.search(p,s,flags=re.I)
            ghz=None
            
            if res:
                print ('res', res, res.group(0))
                s = re.sub(p,'',s, flags=re.I).strip()
                print ('s', s)
                ghz = res.group(1)
            for i in reversed(s.split()):
                if len(i) > 3:
                    last = i
                    break
            if last:
                last = re.split('-|\s',last)[-1]
        return last, ghz


last, ghz= _get_cpu_name_and_ghz(1, s)
print (last, ghz)