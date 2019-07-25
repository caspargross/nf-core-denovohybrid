#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
import re

regexes = {
    'nf-core/denovohybrid': ['v_pipeline.txt', r"(\S+)"],
    'Nextflow': ['v_nextflow.txt', r"(\S+)"],
    'Bandage': ['v_bandage.txt', r"Version:(\S+)"],
    'FastQC': ['v_fastqc.txt', r"FastQC v(\S+)"],
    'Filtlong': ['v_filtlong.txt', r"Filtlong v(\S+)"],
    'miniasm': ['v_miniasm.txt', r"(\S+)"],
    'minimap2': ['v_minimap2.txt', r"(\S+)"],
    'Pilon': ['v_pilon.txt', r"Pilon version(\S+)"],
    'Porechop': ['v_porechop.txt', r"(\S+)"],
    'Quast': ['v_quast.txt', r"QUAST v(\S+)"],
    'Racon': ['v_racon.txt', r"v(\S+)"],
    'Seqtk': ['v_seqtk.txt', r"Version:(\S+)"],
    'Unicycler': ['v_unicycler.txt', r"Unicycler v(\S+)"],
    'wtdbg2': ['v_wtdbg2.txt', r"wtdbg2 (\S+)"],
    'MultiQC': ['v_multiqc.txt', r"multiqc, version (\S+)"],
}
results = OrderedDict()
results['nf-core/denovohybrid'] = '<span style="color:#999999;\">N/A</span>'
results['Nextflow'] = '<span style="color:#999999;\">N/A</span>'
results['FastQC'] = '<span style="color:#999999;\">N/A</span>'
results['MultiQC'] = '<span style="color:#999999;\">N/A</span>'

# Search each file using its regex
for k, v in regexes.items():
    with open(v[0]) as x:
        versions = x.read()
        match = re.search(v[1], versions)
        if match:
            results[k] = "v{}".format(match.group(1))

# Remove software set to false in results
for k in results:
    if not results[k]:
        del(results[k])

# Dump to YAML
print ('''
id: 'software_versions'
section_name: 'nf-core/denovohybrid Software Versions'
section_href: 'https://github.com/nf-core/denovohybrid'
plot_type: 'html'
description: 'are collected at run time from the software output.'
data: |
    <dl class="dl-horizontal">
''')
for k,v in results.items():
    print("        <dt>{}</dt><dd><samp>{}</samp></dd>".format(k,v))
print ("    </dl>")

# Write out regexes as csv file:
with open('software_versions.csv', 'w') as f:
    for k,v in results.items():
        f.write("{}\t{}\n".format(k,v))
