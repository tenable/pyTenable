
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>tenable.ad.directories package &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="_static/custom.css" />
    
    <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
    <script src="_static/jquery.js"></script>
    <script src="_static/underscore.js"></script>
    <script src="_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="search" title="Search" href="search.md" />
    <link rel="next" title="tenable.ad.infrastructure package" href="tenable.ad.infrastructure.md" />
    <link rel="prev" title="tenable.ad.dashboard package" href="tenable.ad.dashboard.md" /> 
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
          <a href="tenable.ad.infrastructure.md" title="tenable.ad.infrastructure package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.dashboard.md" title="tenable.ad.dashboard package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" accesskey="U">tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.directories package</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <section id="module-tenable.ad.directories">
<span id="tenable-ad-directories-package"></span><h1>tenable.ad.directories package<a class="headerlink" href="#module-tenable.ad.directories" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.ad.directories.api">
<span id="tenable-ad-directories-api-module"></span><h2>tenable.ad.directories.api module<a class="headerlink" href="#module-tenable.ad.directories.api" title="Permalink to this headline">¶</a></h2>
<section id="directory">
<h3>Directory<a class="headerlink" href="#directory" title="Permalink to this headline">¶</a></h3>
<p>Methods described in this section relate to the the directory API.
These methods can be accessed at <code class="docutils literal notranslate"><span class="pre">TenableAD.directories</span></code>.</p>
<dl class="py class hide-signature">
<dt class="sig sig-object py" id="tenable.ad.directories.api.DirectoriesAPI">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">DirectoriesAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.directories.api.DirectoriesAPI" title="Permalink to this definition">¶</a></dt>
<dd><dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.directories.api.DirectoriesAPI.create">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">infrastructure_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">dns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.create"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.directories.api.DirectoriesAPI.create" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates a new directory instance.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>infrastructure_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The infrastructure object to bind this directory to.</p></li>
<li><p><strong>name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – Name of the directory instance.</p></li>
<li><p><strong>ip</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The IP Address of the directory server.</p></li>
<li><p><strong>dns</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DNS domain that this directory is tied to.</p></li>
<li><p><strong>directory_type</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The directory’s type.</p></li>
<li><p><strong>ldap_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the LDAP service on the
directory server.</p></li>
<li><p><strong>global_catalog_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Global Catalog service
running on the directory server.</p></li>
<li><p><strong>smb_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Server Messaging
Block (SMB) service running on the directory server.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The created directory instance.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;ExampleServer&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">ip</span><span class="o">=</span><span class="s1">&#39;172.16.0.1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_type</span><span class="o">=</span><span class="s1">&#39;????&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">dns</span><span class="o">=</span><span class="s1">&#39;company.tld&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.directories.api.DirectoriesAPI.delete">
<span class="sig-name descname"><span class="pre">delete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">infrastructure_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">directory_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.delete"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.directories.api.DirectoriesAPI.delete" title="Permalink to this definition">¶</a></dt>
<dd><p>Deletes the directory instance.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>infrastructure_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The infrastructure instance identifier.</p></li>
<li><p><strong>directory_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The directory instance identifier.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="s1">&#39;12&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.directories.api.DirectoriesAPI.details">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">directory_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.directories.api.DirectoriesAPI.details" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the details for a specific directory instance.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>directory_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The directory instance identifier.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the directory object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">details</span><span class="p">(</span><span class="n">directory_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.directories.api.DirectoriesAPI.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.directories.api.DirectoriesAPI.list" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves all directory instances.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The list of directory objects</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">list</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.directories.api.DirectoriesAPI.update">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">infrastructure_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">directory_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.update"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.directories.api.DirectoriesAPI.update" title="Permalink to this definition">¶</a></dt>
<dd><p>Updates the directory instance based on infrastrcture_id and
directory_id.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>infrastructure_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The infrastructure instance identifier.</p></li>
<li><p><strong>directory_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The directory instance identifier.</p></li>
<li><p><strong>name</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – Name of the directory instance.</p></li>
<li><p><strong>ip</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The IP Address of the directory server.</p></li>
<li><p><strong>directory_type</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The directory’s type.</p></li>
<li><p><strong>dns</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DNS domain that this directory is tied to.</p></li>
<li><p><strong>ldap_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The port number associated to the LDAP service on the
directory server.</p></li>
<li><p><strong>global_catalog_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Global Catalog service
running on the directory server.</p></li>
<li><p><strong>smb_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Server Messaging
Block (SMB) service running on the directory server.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The updated directory object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="mi">9</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;updated_new_name&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="mi">9</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;updated_new_name&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">ldap_port</span><span class="o">=</span><span class="mi">390</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">DirectoriesAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id0" title="tenable.base.endpoint.APIEndpoint"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.endpoint.APIEndpoint</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">infrastructure_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">dns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.create"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates a new directory instance.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>infrastructure_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The infrastructure object to bind this directory to.</p></li>
<li><p><strong>name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – Name of the directory instance.</p></li>
<li><p><strong>ip</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The IP Address of the directory server.</p></li>
<li><p><strong>dns</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DNS domain that this directory is tied to.</p></li>
<li><p><strong>directory_type</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The directory’s type.</p></li>
<li><p><strong>ldap_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the LDAP service on the
directory server.</p></li>
<li><p><strong>global_catalog_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Global Catalog service
running on the directory server.</p></li>
<li><p><strong>smb_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Server Messaging
Block (SMB) service running on the directory server.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The created directory instance.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;ExampleServer&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">ip</span><span class="o">=</span><span class="s1">&#39;172.16.0.1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_type</span><span class="o">=</span><span class="s1">&#39;????&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">dns</span><span class="o">=</span><span class="s1">&#39;company.tld&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="id2">
<span class="sig-name descname"><span class="pre">delete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">infrastructure_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">directory_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.delete"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id2" title="Permalink to this definition">¶</a></dt>
<dd><p>Deletes the directory instance.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>infrastructure_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The infrastructure instance identifier.</p></li>
<li><p><strong>directory_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The directory instance identifier.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="s1">&#39;12&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="id3">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">directory_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id3" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the details for a specific directory instance.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>directory_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The directory instance identifier.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the directory object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">details</span><span class="p">(</span><span class="n">directory_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="id4">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id4" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves all directory instances.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The list of directory objects</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">list</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="id5">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">infrastructure_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">directory_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/directories/api.md#DirectoriesAPI.update"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id5" title="Permalink to this definition">¶</a></dt>
<dd><p>Updates the directory instance based on infrastrcture_id and
directory_id.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>infrastructure_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The infrastructure instance identifier.</p></li>
<li><p><strong>directory_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The directory instance identifier.</p></li>
<li><p><strong>name</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – Name of the directory instance.</p></li>
<li><p><strong>ip</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The IP Address of the directory server.</p></li>
<li><p><strong>directory_type</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The directory’s type.</p></li>
<li><p><strong>dns</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DNS domain that this directory is tied to.</p></li>
<li><p><strong>ldap_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The port number associated to the LDAP service on the
directory server.</p></li>
<li><p><strong>global_catalog_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Global Catalog service
running on the directory server.</p></li>
<li><p><strong>smb_port</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The port number associated to the Server Messaging
Block (SMB) service running on the directory server.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The updated directory object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="mi">9</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;updated_new_name&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">directories</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">infrastructure_id</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="mi">9</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;updated_new_name&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">ldap_port</span><span class="o">=</span><span class="mi">390</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

</dd></dl>

</section>
</section>
<section id="module-tenable.ad.directories.schema">
<span id="tenable-ad-directories-schema-module"></span><h2>tenable.ad.directories.schema module<a class="headerlink" href="#module-tenable.ad.directories.schema" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.directories.schema.DirectorySchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">DirectorySchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/directories/schema.md#DirectorySchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.directories.schema.DirectorySchema" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.ad.base.md#tenable.ad.base.schema.CamelCaseSchema" title="tenable.ad.base.schema.CamelCaseSchema"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.ad.base.schema.CamelCaseSchema</span></code></a></p>
</dd></dl>

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
          <a href="tenable.ad.infrastructure.md" title="tenable.ad.infrastructure package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.dashboard.md" title="tenable.ad.dashboard package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" >tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.directories package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>