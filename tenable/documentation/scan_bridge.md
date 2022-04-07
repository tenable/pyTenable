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
        <li class="nav-item nav-item-this"><a href="">tenable.utilities.scan_bridge</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.utilities.scan_bridge</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Scan Bridge</span>
<span class="sd">===========</span>
<span class="sd">The following class allows to send TenableIO scan information</span>
<span class="sd">to a TenableSC repository.</span>
<span class="sd">Usage: ``from tenable.utilities import ScanBridge``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ScanBridge</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">import</span> <span class="nn">os</span>
<span class="kn">from</span> <span class="nn">tenable.io</span> <span class="kn">import</span> <span class="n">TenableIO</span>
<span class="kn">from</span> <span class="nn">tenable.sc</span> <span class="kn">import</span> <span class="n">TenableSC</span>
<div class="viewcode-block" id="ScanBridge"><a class="viewcode-back" href="../../../tenable.utilities.md#tenable.utilities.scan_bridge.ScanBridge">[docs]</a><span class="k">class</span> <span class="nc">ScanBridge</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    The ScanBridge Class can be used as a bridge to send the Tenable.IO scans</span>
<span class="sd">    data to the given Tenable.SC repo_id using the bridge function.</span>
<span class="sd">    Args:</span>
<span class="sd">        tsc (TenableSC object):</span>
<span class="sd">            A TenableSC class object at which scans are to be migrated.</span>
<span class="sd">        tio (TenableIO object):</span>
<span class="sd">            The TenableIO class object where scans details is present.</span>
<span class="sd">    Example:</span>
<span class="sd">        &gt;&gt;&gt; from tenable.utilities import ScanBridge</span>
<span class="sd">        ... from tenable.io import TenableIO</span>
<span class="sd">        ... from tenable.sc import TenableSC</span>
<span class="sd">        ... tsc = TenableSC(username, password, url)</span>
<span class="sd">        ... tio = TenableIO(access_key, secret_key, url)</span>
<span class="sd">        ... sb = ScanBridge(tsc, tio)</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">tsc</span><span class="p">:</span> <span class="n">TenableSC</span><span class="p">,</span> <span class="n">tio</span><span class="p">:</span> <span class="n">TenableIO</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Init method for ScanBridge class.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">tio</span> <span class="o">=</span> <span class="n">tio</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">tsc</span> <span class="o">=</span> <span class="n">tsc</span>
<div class="viewcode-block" id="ScanBridge.bridge"><a class="viewcode-back" href="../../../tenable.utilities.md#tenable.utilities.scan_bridge.ScanBridge.bridge">[docs]</a>    <span class="k">def</span> <span class="nf">bridge</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">scan_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span> <span class="n">repo_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        This method sends the TenableIO scan details to the provided TenableSC repo</span>
<span class="sd">        Args:</span>
<span class="sd">            scan_id (int):</span>
<span class="sd">                The TenableIO scan_id whose details is to be migrated.</span>
<span class="sd">            repo_id (int):</span>
<span class="sd">                The repo_id of Tenable SC instance where scan details</span>
<span class="sd">                will be imported.</span>
<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; sb = ScanBridge(tsc, tio)</span>
<span class="sd">            ... sb.bridge(48,7)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">try</span><span class="p">:</span>
            <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">scan_id</span><span class="si">}</span><span class="s1">.nessus&#39;</span><span class="p">,</span> <span class="s1">&#39;wb&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">nessus</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">tio</span><span class="o">.</span><span class="n">scans</span><span class="o">.</span><span class="n">export</span><span class="p">(</span><span class="n">scan_id</span><span class="p">,</span> <span class="n">fobj</span><span class="o">=</span><span class="n">nessus</span><span class="p">)</span>
                <span class="c1"># self.tio.v3.vm.scans.export(scan_id, fobj=nessus)</span>
            <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">scan_id</span><span class="si">}</span><span class="s1">.nessus&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">file</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">tsc</span><span class="o">.</span><span class="n">scan_instances</span><span class="o">.</span><span class="n">import_scan</span><span class="p">(</span><span class="n">file</span><span class="p">,</span> <span class="n">repo_id</span><span class="p">)</span>
        <span class="k">finally</span><span class="p">:</span>
            <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">exists</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">scan_id</span><span class="si">}</span><span class="s1">.nessus&#39;</span><span class="p">):</span>
                <span class="n">os</span><span class="o">.</span><span class="n">remove</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">scan_id</span><span class="si">}</span><span class="s1">.nessus&#39;</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.utilities.scan_bridge</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>