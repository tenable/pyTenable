
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.scans &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../../_static/custom.css" />
    
    <script data-url_root="../../../" id="documentation_options" src="../../../_static/documentation_options.js"></script>
    <script src="../../../_static/jquery.js"></script>
    <script src="../../../_static/underscore.js"></script>
    <script src="../../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../../genindex.md" />
    <link rel="search" title="Search" href="../../../search.md" /> 
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="../sc.md" accesskey="U">tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.scans</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.scans</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Scans</span>
<span class="sd">=====</span>

<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Scan &lt;Scan.html&gt;` API.  While the api endpoints obliquely refers to the</span>
<span class="sd">model in which this collection of actions modifies as &quot;Scans&quot;, Tenable.sc is</span>
<span class="sd">actually referring to the scan *definitions*, which are the un-launched and/or</span>
<span class="sd">scheduled scans typically seen within the **Active Scans** section within</span>
<span class="sd">Tenable.sc.</span>

<span class="sd">Methods available on ``sc.scans``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ScanAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">UnexpectedValueError</span>

<div class="viewcode-block" id="ScanAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI">[docs]</a><span class="k">class</span> <span class="nc">ScanAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a scan definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># simply verify that the name attribute is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># If the scan type is manually specified, then we will want to make</span>
            <span class="c1"># sure that its a valid input.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;plugin&#39;</span><span class="p">,</span> <span class="s1">&#39;policy&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># The description should always be a string value.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;repo&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># as we accept input as a integer, we need to expand the repository</span>
            <span class="c1"># attribute to be a dictionary item with just the ID (per API docs)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repository&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;repo&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repo&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repo&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;scan_zone&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># similarly to the repository, the API expects the zone to be</span>
            <span class="c1"># defined as a sub-dictionary with just the id field.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;zone&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;scan_zone&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scan_zone&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="mi">0</span><span class="p">)}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scan_zone&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;email_complete&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># As emailOnFinish is effectively a string interpretation of a bool</span>
            <span class="c1"># value, if the snake case equivalent is used, we will convert it</span>
            <span class="c1"># into the expected parameter and remove the snake cased version.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;emailOnFinish&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;email_complete&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;email_complete&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="kc">False</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;email_complete&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;email_launch&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># As emailOnLaunch is effectively a string interpretation of a bool</span>
            <span class="c1"># value, if the snake case equivalent is used, we will convert it</span>
            <span class="c1"># into the expected parameter and remove the snake cased version.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;emailOnLaunch&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;email_launch&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;email_launch&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="kc">False</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;email_launch&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;host_tracking&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># As host_tracking is effectively a string interpretation of a bool</span>
            <span class="c1"># value, if the snake case equivalent is used, we will convert it</span>
            <span class="c1"># into the expected parameter and remove the snake cased version.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dhcpTracking&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;host_tracking&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;host_tracking&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="kc">False</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;host_tracking&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;timeout&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># timeout is the checked version of timeoutAction.  If timeout is</span>
            <span class="c1"># specified, we will check to make sure that the action is a valid</span>
            <span class="c1"># one, put the result into timeoutAction, and remove timeout.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;timeoutAction&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;timeout&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;timeout&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;discard&#39;</span><span class="p">,</span> <span class="s1">&#39;import&#39;</span><span class="p">,</span> <span class="s1">&#39;rollover&#39;</span><span class="p">],</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;import&#39;</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;timeout&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;vhosts&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># As scanningVirtualHosts is effectively a string interpretation of</span>
            <span class="c1"># a bool value, if the snake case equivalent is used, we will</span>
            <span class="c1"># convert it into the expected parameter and remove the snake cased</span>
            <span class="c1"># version.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scanningVirtualHosts&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vhosts&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vhosts&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="kc">False</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vhosts&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;rollover&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># The scan rolloverType parameter simply shortened to better conform</span>
            <span class="c1"># to pythonic naming convention.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;rolloverType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;rollover&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;rollover&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;nextDay&#39;</span><span class="p">,</span> <span class="s1">&#39;template&#39;</span><span class="p">],</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;template&#39;</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;rollover&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;targets&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># targets is list representation of a comma-separated string of</span>
            <span class="c1"># values for the ipList attribute.  By handling as a list instead of</span>
            <span class="c1"># the raw string variant the API expects, we can ensure that there</span>
            <span class="c1"># isn&#39;t any oddities, such as extra spaces, between the commas.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ipList&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;target&#39;</span><span class="p">,</span> <span class="n">i</span><span class="o">.</span><span class="n">strip</span><span class="p">(),</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;targets&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;targets&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;targets&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;max_time&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># maxScanTime is a integer encased in a string value.  the snake</span>
            <span class="c1"># cased version of that expects an integer and converts it into the</span>
            <span class="c1"># string equivalent.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;maxScanTime&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;max_time&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;max_time&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">if</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;maxScanTime&#39;</span><span class="p">]</span> <span class="o">&lt;=</span> <span class="mi">0</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;maxScanTime&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;unlimited&#39;</span><span class="p">;</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;maxScanTime&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;maxScanTime&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;max_time&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;auto_mitigation&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># As classifyMitigatedAge is effectively a string interpretation of</span>
            <span class="c1"># an int value, if the snake case equivalent is used, we will</span>
            <span class="c1"># convert it into the expected parameter and remove the snake cased</span>
            <span class="c1"># version.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;classifyMitigatedAge&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;auto_mitigation&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auto_mitigation&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="mi">0</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auto_mitigation&#39;</span><span class="p">])</span>

        <span class="c1"># hand off the building the schedule sub-document to the schedule</span>
        <span class="c1"># document builder.</span>
        <span class="k">if</span> <span class="s1">&#39;schedule&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;schedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schedule_constructor</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;schedule&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;reports&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># as the reports list should already be in a format that the API</span>
            <span class="c1"># expects, we will simply verify that everything looks like it should.</span>
            <span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;reports&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;reports&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">):</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;report:id&#39;</span><span class="p">,</span> <span class="n">item</span><span class="p">[</span><span class="s1">&#39;id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">),</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;reportSource&#39;</span><span class="p">,</span> <span class="n">item</span><span class="p">[</span><span class="s1">&#39;reportSource&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                    <span class="s1">&#39;cumulative&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;patched&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;individual&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;lce&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;archive&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;mobile&#39;</span>
                <span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;asset_lists&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># asset_lists is the collapsed list of id documents that the API</span>
            <span class="c1"># expects to see.  We will check each item in the list to make sure</span>
            <span class="c1"># its in the right type and then expand it into a sub-document.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;assets&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;asset_list:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;assets_lists&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;asset_lists&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;asset_lists&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;creds&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># creds is the collapsed list of id documents that the API expects</span>
            <span class="c1"># to see.  We will check each item in the list to make sure its in</span>
            <span class="c1"># the right type and then expand it into a sub-document.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;credentials&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;cred:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;creds&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;creds&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;creds&#39;</span><span class="p">])</span>

        <span class="c1"># Lastly, we need to handle the scan types automatically...</span>
        <span class="k">if</span> <span class="s1">&#39;plugin_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="s1">&#39;policy_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># if both are specified, something is wrong here and we should throw</span>
            <span class="c1"># an exception.</span>
            <span class="k">raise</span> <span class="n">UnexpectedValueError</span><span class="p">(</span>
                <span class="s1">&#39;specify either a plugin_id or a policy_id for a scan, not both.&#39;</span><span class="p">)</span>

        <span class="k">elif</span> <span class="s1">&#39;plugin_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># If just the plugin_id is specified, then we are safe to assume</span>
            <span class="c1"># that this is a plugin-based scan.  set the pluginID attribute as</span>
            <span class="c1"># the API would expect and remove the snake cased variant that was</span>
            <span class="c1"># inputted.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;plugin&#39;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;pluginID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">])</span>

        <span class="k">elif</span> <span class="s1">&#39;policy_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># If just the policy_id is specified, then we are safe to assume</span>
            <span class="c1"># that this is a policy-based scan.  set the policy id attribute</span>
            <span class="c1"># within the policy document as the API would expect and remove the</span>
            <span class="c1"># snake cased variant that was inputted.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;policy&#39;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;policy&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;policy_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;policy_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;policy_id&#39;</span><span class="p">])</span>

        <span class="k">return</span> <span class="n">kw</span>

<div class="viewcode-block" id="ScanAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of scan definitions.</span>

<span class="sd">        :sc-api:scan: list &lt;Scan.html#scan_GET&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each scan.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of scan resources.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for scan in sc.scans.list():</span>
<span class="sd">            ...     pprint(scan)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;scan&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">repo</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a scan definition.</span>

<span class="sd">        :sc-api:`scan: create &lt;Scan.html#scan_POST&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str): The name of the scan.</span>
<span class="sd">            repo (int):</span>
<span class="sd">                The repository id for the scan.</span>
<span class="sd">            auto_mitigation (int, optional):</span>
<span class="sd">                How many days to hold on to data before mitigating it?  The</span>
<span class="sd">                default value is 0.</span>
<span class="sd">            asset_lists (list, optional):</span>
<span class="sd">                A list of asset list ids to run the scan against.  A logical OR</span>
<span class="sd">                will be performed to compute what hosts to scan against.</span>
<span class="sd">            creds (list, optional):</span>
<span class="sd">                A list of credential ids to use for the purposes of this scan.</span>
<span class="sd">                This list should be treated as an un-ordered list of credentials.</span>
<span class="sd">            description (str, optional): A description for the scan.</span>
<span class="sd">            email_complete (bool, optional):</span>
<span class="sd">                Should we notify the owner upon completion of the scan?  The</span>
<span class="sd">                default is ``False``.</span>
<span class="sd">            email_launch (bool, optional):</span>
<span class="sd">                Should we notify the owner upon launching the scan?  The default</span>
<span class="sd">                is ``False``.</span>
<span class="sd">            host_tracking (bool, optional):</span>
<span class="sd">                Should DHCP host tracking be enabled?  The default is False.</span>
<span class="sd">            max_time (int, optional):</span>
<span class="sd">                The maximum amount of time that the scan may run in seconds.</span>
<span class="sd">                ``0`` or less for unlimited.</span>
<span class="sd">                The default is ``3600`` seconds.</span>
<span class="sd">            policy_id (int, optional):</span>
<span class="sd">                The policy id to use for a policy-based scan.</span>
<span class="sd">            plugin_id (int, optional):</span>
<span class="sd">                The plugin id to use for a plugin-based scan.</span>
<span class="sd">            reports (list, optional):</span>
<span class="sd">                What reports should be run upon completion of the scan?  Each</span>
<span class="sd">                report dictionary requires an id for the report definition and</span>
<span class="sd">                the source for which to run the report against.  Example:</span>
<span class="sd">                ``{&#39;id&#39;: 1, &#39;reportSource&#39;: &#39;individual&#39;}``.</span>
<span class="sd">            rollover (str, optional):</span>
<span class="sd">                How should rollover scans be created (assuming the scan is</span>
<span class="sd">                configured to create a rollover scan with the timeout action).</span>
<span class="sd">                The available actions are to automatically start the ``nextDay``</span>
<span class="sd">                at the same time the scan was originally configured to run, and</span>
<span class="sd">                to generate a rollover ``template``.  The default action is to</span>
<span class="sd">                generate a ``template``.</span>
<span class="sd">            scan_zone (int, optional):</span>
<span class="sd">                The zone identifier to use for the scan.  If non is selected</span>
<span class="sd">                then the default of &quot;0&quot; or &quot;All Zones&quot; is selected.</span>
<span class="sd">            schedule (dict, optional):</span>
<span class="sd">                A dictionary detailing the repeating schedule of the scan.</span>
<span class="sd">            targets (list, optional):</span>
<span class="sd">                A list of valid targets.  These targets could be IPs, FQDNs,</span>
<span class="sd">                CIDRs, or IP ranges.</span>
<span class="sd">            timeout (str, optional):</span>
<span class="sd">                How should an incomplete scan be handled?  The available actions</span>
<span class="sd">                are ``discard``, ``import``, and ``rollover``.  The default</span>
<span class="sd">                action is ``import``.</span>
<span class="sd">            vhosts (bool, optional):</span>
<span class="sd">                Should virtual host logic be enabled for the scan?  The default</span>
<span class="sd">                is ``False``.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The scan resource for the created scan.</span>

<span class="sd">        Examples:</span>
<span class="sd">            Creating a scan for a single host:</span>

<span class="sd">            &gt;&gt;&gt; sc.scans.create(&#39;Example scan&#39;, 1, policy_id=1001,</span>
<span class="sd">            ...     targets=[&#39;127.0.0.1&#39;])</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repo&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">repo</span>

        <span class="c1"># If the policy_id or plugin_id is set (as one or the other generally</span>
        <span class="c1"># should be) then we will automatically set the scan type based on</span>
        <span class="c1"># which of the values is defined.</span>
        <span class="k">if</span> <span class="s1">&#39;policy_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;policy&#39;</span>
        <span class="k">elif</span> <span class="s1">&#39;plugin_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;plugin&#39;</span>

        <span class="n">scan</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scan&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">scan</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific scan.</span>

<span class="sd">        :sc-api:`scan: details &lt;Scan.html#ScanRESTReference-/scan/{id}&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the scan.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The scan resource record.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; scan = sc.scans.detail(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(scan)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;scan/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits an existing scan definition.</span>

<span class="sd">        :sc-api:`scan: update &lt;Scan.html#scan_id_PATCH&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the scan.</span>
<span class="sd">            auto_mitigation (int, optional):</span>
<span class="sd">                How many days to hold on to data before mitigating it?</span>
<span class="sd">            asset_lists (list, optional):</span>
<span class="sd">                A list of asset list ids to run the scan against.  A logical OR</span>
<span class="sd">                will be performed to compute what hosts to scan against.</span>
<span class="sd">            creds (list, optional):</span>
<span class="sd">                A list of credential ids to use for the purposes of this scan.</span>
<span class="sd">                This list should be treated as an un-ordered list of credentials.</span>
<span class="sd">            description (str, optional): A description for the scan.</span>
<span class="sd">            email_complete (bool, optional):</span>
<span class="sd">                Should we notify the owner upon completion of the scan?</span>
<span class="sd">            email_launch (bool, optional):</span>
<span class="sd">                Should we notify the owner upon launching the scan?</span>
<span class="sd">            host_tracking (bool, optional):</span>
<span class="sd">                Should DHCP host tracking be enabled?</span>
<span class="sd">            max_time (int, optional):</span>
<span class="sd">                The maximum amount of time that the scan may run in seconds.</span>
<span class="sd">                ``0`` or less for unlimited.</span>
<span class="sd">            name (str, optional): The name of the scan.</span>
<span class="sd">            policy (int, optional):</span>
<span class="sd">                The policy id to use for a policy-based scan.</span>
<span class="sd">            plugin (int, optional):</span>
<span class="sd">                The plugin id to use for a plugin-based scan.</span>
<span class="sd">            reports (list, optional):</span>
<span class="sd">                What reports should be run upon completion of the scan?  Each</span>
<span class="sd">                report dictionary requires an id for the report definition and</span>
<span class="sd">                the source for which to run the report against.  Example:</span>
<span class="sd">                ``{&#39;id&#39;: 1, &#39;reportSource&#39;: &#39;individual&#39;}``.</span>
<span class="sd">            repo (int, optional):</span>
<span class="sd">                The repository id for the scan.</span>
<span class="sd">            rollover (str, optional):</span>
<span class="sd">                How should rollover scans be created (assuming the scan is</span>
<span class="sd">                configured to create a rollover scan with the timeout action).</span>
<span class="sd">                The available actions are to automatically start the ``nextDay``</span>
<span class="sd">                at the same time the scan was originally configured to run, and</span>
<span class="sd">                to generate a rollover ``template``.</span>
<span class="sd">            scan_zone (int, optional):</span>
<span class="sd">                The zone identifier to use for the scan.</span>
<span class="sd">            schedule (dict, optional):</span>
<span class="sd">                A dictionary detailing the repeating schedule of the scan.</span>
<span class="sd">            targets (list, optional):</span>
<span class="sd">                A list of valid targets.  These targets could be IPs, FQDNs,</span>
<span class="sd">                CIDRs, or IP ranges.</span>
<span class="sd">            timeout (str, optional):</span>
<span class="sd">                How should an incomplete scan be handled?  The available actions</span>
<span class="sd">                are ``discard``, ``import``, and ``rollover``.</span>
<span class="sd">            vhosts (bool, optional):</span>
<span class="sd">                Should virtual host logic be enabled for the scan?</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The scan resource for the created scan.</span>

<span class="sd">        Examples:</span>
<span class="sd">            Editing an existing scan&#39;s name:</span>

<span class="sd">            &gt;&gt;&gt; sc.scans.edit(1, name=&#39;Example scan&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">scan</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;scan/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">json</span><span class="o">=</span><span class="n">scan</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes the specified scan from SecurityCenter.</span>

<span class="sd">        :sc-api:`scan: delete &lt;Scan.html#scan_id_DELETE&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the scan to delete.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                The list of scan id removed.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scans.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;scan/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">))</span>
            <span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanAPI.copy"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI.copy">[docs]</a>    <span class="k">def</span> <span class="nf">copy</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">user_id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Copies an existing scan definition.</span>

<span class="sd">        :sc-api:`scan: copy &lt;Scan.html#ScanRESTReference-/scan/{id}/copyScanCopyPOST&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The scan definition identifier to copy.</span>
<span class="sd">            name (str): The name of the copy that&#39;s created.</span>
<span class="sd">            user_id (int):</span>
<span class="sd">                The user id to assign as the owner of the new scan definition.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                Scan definition resource.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scans.copy(1, name=&#39;Cloned Scan&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="nb">str</span><span class="p">),</span>
            <span class="s1">&#39;targetUser&#39;</span><span class="p">:</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;user_id&#39;</span><span class="p">,</span> <span class="n">user_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
        <span class="p">}</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scan/</span><span class="si">{}</span><span class="s1">/copy&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="s1">&#39;scan&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanAPI.launch"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scans.ScanAPI.launch">[docs]</a>    <span class="k">def</span> <span class="nf">launch</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">diagnostic_target</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">diagnostic_password</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Launches a scan definition.</span>

<span class="sd">        :sc-api:`scan: launch &lt;Scan.html#ScanRESTReference-/scan/{id}/launch&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The scan definition identifier to launch.</span>
<span class="sd">            diagnostic_target (str, optional):</span>
<span class="sd">                A valid IP or hostname to launch a diagnostic scan against.  The</span>
<span class="sd">                ``diagnostic_password`` must also be specified or else this</span>
<span class="sd">                parameter will be ignored.</span>
<span class="sd">            diagnostic_password (str, optional):</span>
<span class="sd">                A password to use for the diagnostic scan.  The</span>
<span class="sd">                ``diagnostic_target`` must also be specified or else this</span>
<span class="sd">                parameter will be ignored.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                A scan result resource for the newly launched scan.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; running = sc.scans.launch(1)</span>
<span class="sd">            &gt;&gt;&gt; print(&#39;The Scan Result ID is {}&#39;.format(</span>
<span class="sd">            ...     running[&#39;scanResult&#39;][&#39;id&#39;]))</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">diagnostic_target</span> <span class="ow">and</span> <span class="n">diagnostic_password</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;diagnosticTarget&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;diagnostic_target&#39;</span><span class="p">,</span> <span class="n">diagnostic_target</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;diagnosticPassword&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;diagnostic_password&#39;</span><span class="p">,</span> <span class="n">diagnostic_password</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scan/</span><span class="si">{}</span><span class="s1">/launch&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
</pre></div>

            <div class="clearer"></div>
          </div>
      </div>
      <div class="clearer"></div>
    </div>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="../sc.md" >tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.scans</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>