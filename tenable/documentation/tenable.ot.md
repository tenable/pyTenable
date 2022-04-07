<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="next" title="tenable.ot.graphql package" href="tenable.ot.graphql.md" />
    <link rel="prev" title="tenable.nessus package" href="tenable.nessus.md" /> 
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
          <a href="tenable.ot.graphql.md" title="tenable.ot.graphql package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.nessus.md" title="tenable.nessus package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ot package</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <section id="module-tenable.ot">
<span id="tenable-ot-package"></span><h1>tenable.ot package<a class="headerlink" href="#module-tenable.ot" title="Permalink to this headline">¶</a></h1>
<p>Tenable.ot Base Package</p>
<section id="subpackages">
<h2>Subpackages<a class="headerlink" href="#subpackages" title="Permalink to this headline">¶</a></h2>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="tenable.ot.graphql.md">tenable.ot.graphql package</a><ul>
<li class="toctree-l2"><a class="reference internal" href="tenable.ot.graphql.md#submodules">Submodules</a></li>
<li class="toctree-l2"><a class="reference internal" href="tenable.ot.graphql.md#module-tenable.ot.graphql.assets">tenable.ot.graphql.assets module</a></li>
<li class="toctree-l2"><a class="reference internal" href="tenable.ot.graphql.md#module-tenable.ot.graphql.definitions">tenable.ot.graphql.definitions module</a></li>
<li class="toctree-l2"><a class="reference internal" href="tenable.ot.graphql.md#module-tenable.ot.graphql.iterators">tenable.ot.graphql.iterators module</a></li>
</ul>
</li>
</ul>
</div>
</section>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.ot.assets">
<span id="tenable-ot-assets-module"></span><h2>tenable.ot.assets module<a class="headerlink" href="#module-tenable.ot.assets" title="Permalink to this headline">¶</a></h2>
<section id="assets">
<h3>Assets<a class="headerlink" href="#assets" title="Permalink to this headline">¶</a></h3>
<p>Methods described in this section relate to the the assets API.
These methods can be accessed at <code class="docutils literal notranslate"><span class="pre">TenableOT.assets</span></code>.</p>
<dl class="py class hide-signature">
<dt class="sig sig-object py" id="tenable.ot.assets.AssetsAPI">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">AssetsAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/assets.md#AssetsAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ot.assets.AssetsAPI" title="Permalink to this definition">¶</a></dt>
<dd><dl class="py method">
<dt class="sig sig-object py" id="tenable.ot.assets.AssetsAPI.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">filter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">search</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sort</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">start_at</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">limit</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">200</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/assets.md#AssetsAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ot.assets.AssetsAPI.list" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves a list of assets via the GraphQL API.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>filter</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – A document as defined by Tenable.ot online documentation.</p></li>
<li><p><strong>search</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – A search string to further limit the response.</p></li>
<li><p><strong>sort</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)"><em>list</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>]</em><em>, </em><em>optional</em>) – A list of order documents, each of which must contain both the
<code class="docutils literal notranslate"><span class="pre">field</span></code> and <code class="docutils literal notranslate"><span class="pre">direction</span></code> keys and may also contain the
optional <code class="docutils literal notranslate"><span class="pre">function</span></code> key. Default sort is by descending id
order. Please refer to Tenable.ot online documentation for more
information.</p></li>
<li><p><strong>start_at</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The cursor to start the scan from (the default is an empty
cursor).</p></li>
<li><p><strong>limit</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – Max number of objects that get retrieved per page (the default
is 200).</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>An iterator object that will handle pagination of the data.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><code class="xref py py-obj docutils literal notranslate"><span class="pre">OTGraphIterator</span></code></p>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span>    <span class="k">for</span> <span class="n">asset</span> <span class="ow">in</span> <span class="n">tot</span><span class="o">.</span><span class="n">assets</span><span class="o">.</span><span class="n">list</span><span class="p">(</span><span class="n">limit</span><span class="o">=</span><span class="mi">500</span><span class="p">):</span>
<span class="go">            print(asset)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">AssetsAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/assets.md#AssetsAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id0" title="tenable.base.endpoint.APIEndpoint"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.endpoint.APIEndpoint</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">filter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">search</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sort</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">start_at</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">limit</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">200</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/assets.md#AssetsAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves a list of assets via the GraphQL API.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>filter</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – A document as defined by Tenable.ot online documentation.</p></li>
<li><p><strong>search</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – A search string to further limit the response.</p></li>
<li><p><strong>sort</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)"><em>list</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>]</em><em>, </em><em>optional</em>) – A list of order documents, each of which must contain both the
<code class="docutils literal notranslate"><span class="pre">field</span></code> and <code class="docutils literal notranslate"><span class="pre">direction</span></code> keys and may also contain the
optional <code class="docutils literal notranslate"><span class="pre">function</span></code> key. Default sort is by descending id
order. Please refer to Tenable.ot online documentation for more
information.</p></li>
<li><p><strong>start_at</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The cursor to start the scan from (the default is an empty
cursor).</p></li>
<li><p><strong>limit</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – Max number of objects that get retrieved per page (the default
is 200).</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>An iterator object that will handle pagination of the data.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><code class="xref py py-obj docutils literal notranslate"><span class="pre">OTGraphIterator</span></code></p>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span>    <span class="k">for</span> <span class="n">asset</span> <span class="ow">in</span> <span class="n">tot</span><span class="o">.</span><span class="n">assets</span><span class="o">.</span><span class="n">list</span><span class="p">(</span><span class="n">limit</span><span class="o">=</span><span class="mi">500</span><span class="p">):</span>
<span class="go">            print(asset)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
</section>
</section>
<section id="module-tenable.ot.session">
<span id="tenable-ot-session-module"></span><h2>tenable.ot.session module<a class="headerlink" href="#module-tenable.ot.session" title="Permalink to this headline">¶</a></h2>
<section id="tenable-ot">
<h3>Tenable.ot<a class="headerlink" href="#tenable-ot" title="Permalink to this headline">¶</a></h3>
<p>This package covers the Tenable.ot interface.</p>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ot.session.TenableOT">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">TenableOT</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/session.md#TenableOT"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ot.session.TenableOT" title="Permalink to this definition">¶</a></dt>
<dd><p>The Tenable.ot object is the primary interaction point for users to
interface with Tenable.io via the pyTenable library.  All of the API
endpoint classes that have been written will be grafted onto this class.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>api_key</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The user’s API key for Tenable.ot.  If an api key isn’t specified,
then the library will attempt to read the environment variable
<code class="docutils literal notranslate"><span class="pre">TOT_API_KEY</span></code> to acquire the key.</p></li>
<li><p><strong>url</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The base URL used to connect to the Tenable.ot application.  If a
url isn’t specified, then the library will attempt to read the
environment variable <code class="docutils literal notranslate"><span class="pre">TOT_URL</span></code> to acquire the URL.</p></li>
<li><p><strong>**kwargs</strong> – arguments passed to <a class="reference internal" href="tenable.base.md#id1" title="tenable.base.platform.APIPlatform"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.platform.APIPlatform</span></code></a> for
connection management.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>Basic Example:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tenable.ot</span> <span class="kn">import</span> <span class="n">TenableOT</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span> <span class="o">=</span> <span class="n">TenableOT</span><span class="p">(</span><span class="n">secret_key</span><span class="o">=</span><span class="s1">&#39;SECRET_KEY&#39;</span><span class="p">,</span>
<span class="go">..                 url=&#39;https://ot.example.com&#39;)</span>
</pre></div>
</div>
<p>Example with proper identification:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span> <span class="o">=</span> <span class="n">TenableOT</span><span class="p">(</span><span class="n">secret_key</span><span class="o">=</span><span class="s1">&#39;SECRET_KEY&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">url</span><span class="o">=</span><span class="s1">&#39;https://ot.example.com&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company Name&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">product</span><span class="o">=</span><span class="s1">&#39;My Awesome Widget&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>Example with proper identification leveraging environment variables for
the connection parameters:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span> <span class="o">=</span> <span class="n">TenableOT</span><span class="p">(</span><span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company&#39;</span><span class="p">,</span> <span class="n">product</span><span class="o">=</span><span class="s1">&#39;Widget&#39;</span><span class="p">,</span> <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ot.session.TenableOT.graphql">
<span class="sig-name descname"><span class="pre">graphql</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/session.md#TenableOT.graphql"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ot.session.TenableOT.graphql" title="Permalink to this definition">¶</a></dt>
<dd><p>GraphQL Endpoint</p>
<p>This singular method exposes the GraphQL API to the library.  As all
keyword arguments are passed directly to the JSON body, it allows for a
freeform interface into the GraphQL API.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – The key/values that should be passed to the body of the GraphQL
request.</p>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span><span class="o">.</span><span class="n">graphql</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">variables</span><span class="o">=</span><span class="p">{</span><span class="s1">&#39;asset&#39;</span><span class="p">:</span> <span class="s1">&#39;b64 id string&#39;</span><span class="p">},</span>
<span class="gp">... </span>    <span class="n">query</span><span class="o">=</span><span class="s1">&#39;&#39;&#39;</span>
<span class="gp">... </span><span class="s1">        query getAssetDetails($asset: ID!) {</span>
<span class="gp">... </span><span class="s1">            asset(id: $asset) {</span>
<span class="gp">... </span><span class="s1">                id</span>
<span class="gp">... </span><span class="s1">                type</span>
<span class="gp">... </span><span class="s1">                name</span>
<span class="gp">... </span><span class="s1">                criticality</span>
<span class="gp">... </span><span class="s1">                location</span>
<span class="gp">... </span><span class="s1">            }</span>
<span class="gp">... </span><span class="s1">        }</span>
<span class="gp">... </span><span class="s1">&#39;&#39;&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
<div class="toctree-wrapper compound">
</div>
<dl class="py class">
<dt class="sig sig-object py" id="id2">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">TenableOT</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/session.md#TenableOT"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id2" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id1" title="tenable.base.platform.APIPlatform"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.platform.APIPlatform</span></code></a></p>
<p>The Tenable.ot object is the primary interaction point for users to
interface with Tenable.io via the pyTenable library.  All of the API
endpoint classes that have been written will be grafted onto this class.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>api_key</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The user’s API key for Tenable.ot.  If an api key isn’t specified,
then the library will attempt to read the environment variable
<code class="docutils literal notranslate"><span class="pre">TOT_API_KEY</span></code> to acquire the key.</p></li>
<li><p><strong>url</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The base URL used to connect to the Tenable.ot application.  If a
url isn’t specified, then the library will attempt to read the
environment variable <code class="docutils literal notranslate"><span class="pre">TOT_URL</span></code> to acquire the URL.</p></li>
<li><p><strong>**kwargs</strong> – arguments passed to <a class="reference internal" href="tenable.base.md#id1" title="tenable.base.platform.APIPlatform"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.platform.APIPlatform</span></code></a> for
connection management.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>Basic Example:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tenable.ot</span> <span class="kn">import</span> <span class="n">TenableOT</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span> <span class="o">=</span> <span class="n">TenableOT</span><span class="p">(</span><span class="n">secret_key</span><span class="o">=</span><span class="s1">&#39;SECRET_KEY&#39;</span><span class="p">,</span>
<span class="go">..                 url=&#39;https://ot.example.com&#39;)</span>
</pre></div>
</div>
<p>Example with proper identification:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span> <span class="o">=</span> <span class="n">TenableOT</span><span class="p">(</span><span class="n">secret_key</span><span class="o">=</span><span class="s1">&#39;SECRET_KEY&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">url</span><span class="o">=</span><span class="s1">&#39;https://ot.example.com&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company Name&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">product</span><span class="o">=</span><span class="s1">&#39;My Awesome Widget&#39;</span><span class="p">,</span>
<span class="gp">... </span>               <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>Example with proper identification leveraging environment variables for
the connection parameters:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span> <span class="o">=</span> <span class="n">TenableOT</span><span class="p">(</span><span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company&#39;</span><span class="p">,</span> <span class="n">product</span><span class="o">=</span><span class="s1">&#39;Widget&#39;</span><span class="p">,</span> <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="id3">
<span class="sig-name descname"><span class="pre">graphql</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ot/session.md#TenableOT.graphql"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id3" title="Permalink to this definition">¶</a></dt>
<dd><p>GraphQL Endpoint</p>
<p>This singular method exposes the GraphQL API to the library.  As all
keyword arguments are passed directly to the JSON body, it allows for a
freeform interface into the GraphQL API.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – The key/values that should be passed to the body of the GraphQL
request.</p>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">ot</span><span class="o">.</span><span class="n">graphql</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">variables</span><span class="o">=</span><span class="p">{</span><span class="s1">&#39;asset&#39;</span><span class="p">:</span> <span class="s1">&#39;b64 id string&#39;</span><span class="p">},</span>
<span class="gp">... </span>    <span class="n">query</span><span class="o">=</span><span class="s1">&#39;&#39;&#39;</span>
<span class="gp">... </span><span class="s1">        query getAssetDetails($asset: ID!) {</span>
<span class="gp">... </span><span class="s1">            asset(id: $asset) {</span>
<span class="gp">... </span><span class="s1">                id</span>
<span class="gp">... </span><span class="s1">                type</span>
<span class="gp">... </span><span class="s1">                name</span>
<span class="gp">... </span><span class="s1">                criticality</span>
<span class="gp">... </span><span class="s1">                location</span>
<span class="gp">... </span><span class="s1">            }</span>
<span class="gp">... </span><span class="s1">        }</span>
<span class="gp">... </span><span class="s1">&#39;&#39;&#39;</span><span class="p">)</span>
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
          <a href="tenable.ot.graphql.md" title="tenable.ot.graphql package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.nessus.md" title="tenable.nessus package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ot package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>