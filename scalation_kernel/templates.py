
from mako.template import Template

info_template = Template("""
<p><strong>Pretty Print Information</strong></p>
<table>
  <tr>
    <td>Name</td><td>${name}</td>
  </tr>
  <tr>
    <td>Type</td><td>${type}</td>
  </tr>
  <tr>
    <td>Value</td><td>${value}</td>
  </tr>
</table>
<p><i>In the future, we should be able to use the above information to better display the result in Jupyter.</i></p>
""")

vector_template = Template("""
<div style='overflow:auto;'>
<table>
  <tr>
    <td><strong>Index</strong></td>
% for elem in elems:
    <td>${loop.index}</td>
% endfor
  </tr>
  <tr>
    <td><strong>Value</strong></td>
% for elem in elems:
    <td>${elem}</td>
% endfor
  </tr>
</table>
</div>

<div id="chart_${name}_div"></div>
<p>
Charts: 
<a id="chart_${name}_line" href="#">Line</a>, 
<a id="chart_${name}_bar" href="#">Bar</a>
</p>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
google.charts.load('current', {packages: ['corechart', 'line', 'bar']});
google.charts.setOnLoadCallback(function() {
var data = new google.visualization.DataTable();
      data.addColumn('number', 'Index');
      data.addColumn('number', 'Value');
      data.addRows([
% for elem in elems:
        [${loop.index}, ${elem}],
% endfor
      ]);
      var options = {
        hAxis: {
          title: 'Index'
        },
        vAxis: {
          title: 'Value'
        }
      };
      
      document.getElementById('chart_${name}_line').onclick = function() {
        var chart = new google.visualization.LineChart(document.getElementById('chart_${name}_div'));
        chart.draw(data, options);
      }

      document.getElementById('chart_${name}_bar').onclick = function() {
        var chart = new google.visualization.ColumnChart(document.getElementById('chart_${name}_div'));
        chart.draw(data, options);
      }

});
</script>
""")

