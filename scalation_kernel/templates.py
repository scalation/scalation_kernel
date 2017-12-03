
from mako.template import Template

toggle_debug_mode_template = Template("""
<p>
% if debug_mode:
<strong>ScalaTion Kernel <code>debug_mode</code> enabled.</strong>
The kernel will now, as needed, respond with additional messages containing debug information.
% else:
<strong>ScalaTion Kernel <code>debug_mode</code> disabled.</strong>
% endif
To undo this setting, use the <code>::debug_mode</code> command again.
</p>
""")

debug_template = Template("""
<style>
#stack-${uuid} {
    display: none;
}

#stack-${uuid} code {
    white-space: pre;
    overflow-x: auto;
    display: inline-block;
    min-width: 100%;
}
</style>
<p><strong>ScalaTion Kernel Debug:</strong> ${timestamp} -- ${message} [<a id="toggle-${uuid}">toggle stack trace</a>]</p>
<pre id="stack-${uuid}"><code>
% for frameinfo in stack:
${str(frameinfo)}
% endfor
</code></pre>
<script>
$("#toggle-${uuid}").click(function(){
    $("#stack-${uuid}").toggle();
});
</script>
""")

prettyr_template = Template("""
<p><strong>Relation: ${name}</strong></p>
<table>
<tr>
% for colName in colNames:
    <th><code>${colName}</code></th>
% endfor
</tr>
% for row in data:
<tr>
    % for item in row:
    <td><code>${item}</code></td>
    % endfor
</tr>
% endfor 
</table>
""")

