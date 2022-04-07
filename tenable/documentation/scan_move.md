<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../../genindex.md" />
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
          <li class="nav-item nav-item-1"><a href="../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.utilities.scan_move</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.utilities.scan_move</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Scan Move</span>
<span class="sd">=========</span>
<span class="sd">The following class allows to send scans from one instance of TenableIO to</span>
<span class="sd">another instance of TenableIO.</span>
<span class="sd">Methods available on ``tio.utilities.scan_move``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ScanMove</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">tenable.io</span> <span class="kn">import</span> <span class="n">TenableIO</span>
<div class="viewcode-block" id="ScanMove"><a class="viewcode-back" href="../../../tenable.utilities.scan_move.md#tenable.utilities.scan_move.ScanMove">[docs]</a><span class="k">class</span> <span class="nc">ScanMove</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This will contain all methods related to Users</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">source_tio</span><span class="p">:</span> <span class="n">TenableIO</span><span class="p">,</span> <span class="n">target_tio</span><span class="p">:</span> <span class="n">TenableIO</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">source_tio</span> <span class="o">=</span> <span class="n">source_tio</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">target_tio</span> <span class="o">=</span> <span class="n">target_tio</span>
    <span class="k">def</span> <span class="nf">_get_scan_history</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">scan_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">limit</span><span class="p">:</span> <span class="nb">int</span><span class="p">):</span>
        <span class="c1"># get scan history using scan id</span>
        <span class="n">scan_history</span> <span class="o">=</span> <span class="p">[]</span>
        <span class="n">count</span> <span class="o">=</span> <span class="mi">0</span>
        <span class="k">for</span> <span class="n">scan_instance</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">source_tio</span><span class="o">.</span><span class="n">v3</span><span class="o">.</span><span class="n">vm</span><span class="o">.</span><span class="n">scans</span><span class="o">.</span><span class="n">history</span><span class="p">(</span><span class="n">scan_id</span><span class="p">):</span>
            <span class="k">if</span> <span class="n">count</span> <span class="o">==</span> <span class="n">limit</span><span class="p">:</span>
                <span class="k">break</span>
            <span class="k">if</span> <span class="n">scan_instance</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;status&#39;</span><span class="p">,</span> <span class="s1">&#39;&#39;</span><span class="p">)</span> <span class="o">==</span> <span class="s1">&#39;completed&#39;</span><span class="p">:</span>
                <span class="n">count</span> <span class="o">+=</span> <span class="mi">1</span>
                <span class="n">scan_history</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">scan_instance</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">))</span>
        <span class="k">return</span> <span class="n">scan_history</span>
<div class="viewcode-block" id="ScanMove.move"><a class="viewcode-back" href="../../../tenable.utilities.scan_move.md#tenable.utilities.scan_move.ScanMove.move">[docs]</a>    <span class="k">def</span> <span class="nf">move</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">limit</span><span class="p">):</span>
        <span class="c1"># get all scans from source instance</span>
        <span class="n">scan_filter</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;and&#39;</span><span class="p">:</span> <span class="p">[</span>
                <span class="p">{</span><span class="s1">&#39;property&#39;</span><span class="p">:</span> <span class="s1">&#39;status&#39;</span><span class="p">,</span> <span class="s1">&#39;operator&#39;</span><span class="p">:</span> <span class="s1">&#39;eq&#39;</span><span class="p">,</span> <span class="s1">&#39;value&#39;</span><span class="p">:</span> <span class="s1">&#39;completed&#39;</span><span class="p">},</span>
                <span class="p">{</span><span class="s1">&#39;property&#39;</span><span class="p">:</span> <span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="s1">&#39;operator&#39;</span><span class="p">:</span> <span class="s1">&#39;eq&#39;</span><span class="p">,</span> <span class="s1">&#39;value&#39;</span><span class="p">:</span> <span class="s1">&#39;remote&#39;</span><span class="p">}</span>
            <span class="p">]</span>
        <span class="p">}</span></div></div>
        <span class="c1"># TODO Search has not implemented yet</span>
        <span class="c1"># for mv_scan in self.source_tio.v3.vm.scans.search(</span>
        <span class="c1">#     filter=scan_filter</span>
        <span class="c1"># ):</span>
        <span class="c1">#     scan_history = self._get_scan_history(mv_scan[&#39;id&#39;], limit)</span>
        <span class="c1">#</span>
        <span class="c1">#     for scan in scan_history:</span>
        <span class="c1">#         print(&quot;Exporting Scan ID:{}, with history_id: {} now\n&quot;.format(</span>
        <span class="c1">#             mv_scan, scan</span>
        <span class="c1">#         ))</span>
        <span class="c1">#</span>
        <span class="c1">#         scan_report = self.source_tio.v3.scans.export(scan)</span>
        <span class="c1">#         imported_scan = self.target_tio.v3.scans.import_scan(</span>
        <span class="c1">#             scan_report</span>
        <span class="c1">#         )</span>
        <span class="c1">#</span>
        <span class="c1">#         print(&quot;Scan imported: {}&quot;.format(</span>
        <span class="c1">#             imported_scan.get(&#39;scan&#39;).get(&#39;id&#39;)</span>
        <span class="c1">#         ))</span>
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
        <li class="nav-item nav-item-this"><a href="">tenable.utilities.scan_move</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>