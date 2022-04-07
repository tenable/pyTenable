<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="next" title="tenable.utilities.scan_move package" href="tenable.utilities.scan_move.md" />
    <link rel="prev" title="tenable.sc package" href="tenable.sc.md" /> 
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="right" >
          <a href="tenable.utilities.scan_move.md" title="tenable.utilities.scan_move package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.sc.md" title="tenable.sc package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.utilities package</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <section id="module-tenable.utilities">
<span id="tenable-utilities-package"></span><h1>tenable.utilities package<a class="headerlink" href="#module-tenable.utilities" title="Permalink to this headline">¶</a></h1>
<section id="subpackages">
<h2>Subpackages<a class="headerlink" href="#subpackages" title="Permalink to this headline">¶</a></h2>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="tenable.utilities.scan_move.md">tenable.utilities.scan_move package</a><ul>
<li class="toctree-l2"><a class="reference internal" href="tenable.utilities.scan_move.md#scan-move">Scan Move</a></li>
</ul>
</li>
</ul>
</div>
</section>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.utilities.scan_bridge">
<span id="tenable-utilities-scan-bridge-module"></span><h2>tenable.utilities.scan_bridge module<a class="headerlink" href="#module-tenable.utilities.scan_bridge" title="Permalink to this headline">¶</a></h2>
<section id="scan-bridge">
<h3>Scan Bridge<a class="headerlink" href="#scan-bridge" title="Permalink to this headline">¶</a></h3>
<p>The following class allows to send TenableIO scan information
to a TenableSC repository.</p>
<p>Usage: <code class="docutils literal notranslate"><span class="pre">from</span> <span class="pre">tenable.utilities</span> <span class="pre">import</span> <span class="pre">ScanBridge</span></code>:</p>
<dl class="py class hide-signature">
<dt class="sig sig-object py" id="tenable.utilities.scan_bridge.ScanBridge">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">ScanBridge</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">tsc</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="tenable.sc.md#id0" title="tenable.sc.TenableSC"><span class="pre">tenable.sc.TenableSC</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">tio</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tenable.io.TenableIO</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/utilities/scan_bridge.md#ScanBridge"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.utilities.scan_bridge.ScanBridge" title="Permalink to this definition">¶</a></dt>
<dd><p>The ScanBridge Class can be used as a bridge to send the Tenable.IO scans
data to the given Tenable.SC repo_id using the bridge function.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>tsc</strong> (<em>TenableSC object</em>) – A TenableSC class object at which scans are to be migrated.</p></li>
<li><p><strong>tio</strong> (<em>TenableIO object</em>) – The TenableIO class object where scans details is present.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tenable.utilities</span> <span class="kn">import</span> <span class="n">ScanBridge</span>
<span class="gp">... </span><span class="kn">from</span> <span class="nn">tenable.io</span> <span class="kn">import</span> <span class="n">TenableIO</span>
<span class="gp">... </span><span class="kn">from</span> <span class="nn">tenable.sc</span> <span class="kn">import</span> <span class="n">TenableSC</span>
<span class="gp">... </span><span class="n">tsc</span> <span class="o">=</span> <span class="n">TenableSC</span><span class="p">(</span><span class="n">username</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span>
<span class="gp">... </span><span class="n">tio</span> <span class="o">=</span> <span class="n">TenableIO</span><span class="p">(</span><span class="n">access_key</span><span class="p">,</span> <span class="n">secret_key</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span>
<span class="gp">... </span><span class="n">sb</span> <span class="o">=</span> <span class="n">ScanBridge</span><span class="p">(</span><span class="n">tsc</span><span class="p">,</span> <span class="n">tio</span><span class="p">)</span>
</pre></div>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.utilities.scan_bridge.ScanBridge.bridge">
<span class="sig-name descname"><span class="pre">bridge</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">scan_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">repo_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="reference internal" href="_modules/tenable/utilities/scan_bridge.md#ScanBridge.bridge"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.utilities.scan_bridge.ScanBridge.bridge" title="Permalink to this definition">¶</a></dt>
<dd><p>This method sends the TenableIO scan details to the provided TenableSC repo</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>scan_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The TenableIO scan_id whose details is to be migrated.</p></li>
<li><p><strong>repo_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The repo_id of Tenable SC instance where scan details
will be imported.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">sb</span> <span class="o">=</span> <span class="n">ScanBridge</span><span class="p">(</span><span class="n">tsc</span><span class="p">,</span> <span class="n">tio</span><span class="p">)</span>
<span class="gp">... </span><span class="n">sb</span><span class="o">.</span><span class="n">bridge</span><span class="p">(</span><span class="mi">48</span><span class="p">,</span><span class="mi">7</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">ScanBridge</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">tsc</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="tenable.sc.md#id0" title="tenable.sc.TenableSC"><span class="pre">tenable.sc.TenableSC</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">tio</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tenable.io.TenableIO</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/utilities/scan_bridge.md#ScanBridge"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference external" href="https://docs.python.org/3/library/functions.html#object" title="(in Python v3.10)"><code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></a></p>
<p>The ScanBridge Class can be used as a bridge to send the Tenable.IO scans
data to the given Tenable.SC repo_id using the bridge function.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>tsc</strong> (<em>TenableSC object</em>) – A TenableSC class object at which scans are to be migrated.</p></li>
<li><p><strong>tio</strong> (<em>TenableIO object</em>) – The TenableIO class object where scans details is present.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tenable.utilities</span> <span class="kn">import</span> <span class="n">ScanBridge</span>
<span class="gp">... </span><span class="kn">from</span> <span class="nn">tenable.io</span> <span class="kn">import</span> <span class="n">TenableIO</span>
<span class="gp">... </span><span class="kn">from</span> <span class="nn">tenable.sc</span> <span class="kn">import</span> <span class="n">TenableSC</span>
<span class="gp">... </span><span class="n">tsc</span> <span class="o">=</span> <span class="n">TenableSC</span><span class="p">(</span><span class="n">username</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span>
<span class="gp">... </span><span class="n">tio</span> <span class="o">=</span> <span class="n">TenableIO</span><span class="p">(</span><span class="n">access_key</span><span class="p">,</span> <span class="n">secret_key</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span>
<span class="gp">... </span><span class="n">sb</span> <span class="o">=</span> <span class="n">ScanBridge</span><span class="p">(</span><span class="n">tsc</span><span class="p">,</span> <span class="n">tio</span><span class="p">)</span>
</pre></div>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">bridge</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">scan_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">repo_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="reference internal" href="_modules/tenable/utilities/scan_bridge.md#ScanBridge.bridge"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>This method sends the TenableIO scan details to the provided TenableSC repo</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>scan_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The TenableIO scan_id whose details is to be migrated.</p></li>
<li><p><strong>repo_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The repo_id of Tenable SC instance where scan details
will be imported.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">sb</span> <span class="o">=</span> <span class="n">ScanBridge</span><span class="p">(</span><span class="n">tsc</span><span class="p">,</span> <span class="n">tio</span><span class="p">)</span>
<span class="gp">... </span><span class="n">sb</span><span class="o">.</span><span class="n">bridge</span><span class="p">(</span><span class="mi">48</span><span class="p">,</span><span class="mi">7</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
</section>
</section>
</section>
            <div class="clearer"></div>
          </div>
      </div>
      <div class="clearer"></div>
    </div>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="right" >
          <a href="tenable.utilities.scan_move.md" title="tenable.utilities.scan_move package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.sc.md" title="tenable.sc package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.utilities package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>