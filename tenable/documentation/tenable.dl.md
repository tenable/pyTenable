<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="next" title="tenable.io package" href="tenable.io.md" />
    <link rel="prev" title="tenable.base.utils package" href="tenable.base.utils.md" /> 
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
          <a href="tenable.io.md" title="tenable.io package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.base.utils.md" title="tenable.base.utils package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.dl package</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <section id="module-tenable.dl">
<span id="tenable-dl-package"></span><h1>tenable.dl package<a class="headerlink" href="#module-tenable.dl" title="Permalink to this headline">¶</a></h1>
<section id="product-downloads">
<h2>Product Downloads<a class="headerlink" href="#product-downloads" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.dl.Downloads">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">Downloads</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api_token</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.dl.Downloads" title="Permalink to this definition">¶</a></dt>
<dd><p>The Downloads object is the primary interaction point for users to
interface with Downloads API via the pyTenable library.  All of the API
endpoint classes that have been written will be grafted onto this class.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>api_token</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The user’s API access key for Tenable.io  If an access key isn’t
specified, then the library will attempt to read the environment
variable <code class="docutils literal notranslate"><span class="pre">TDL_API_TOKEN</span></code> to acquire the key.</p></li>
<li><p><strong>retries</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – The number of retries to make before failing a request.  The
default is <code class="docutils literal notranslate"><span class="pre">5</span></code>.</p></li>
<li><p><strong>backoff</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.10)"><em>float</em></a><em>, </em><em>optional</em>) – If a 429 response is returned, how much do we want to backoff
if the response didn’t send a Retry-After header.  The default
backoff is <code class="docutils literal notranslate"><span class="pre">1</span></code> second.</p></li>
<li><p><strong>vendor</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The vendor name for the User-Agent string.</p></li>
<li><p><strong>product</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The product name for the User-Agent string.</p></li>
<li><p><strong>build</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The version or build identifier for the User-Agent string.</p></li>
<li><p><strong>timeout</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – The connection timeout parameter informing the library how long to
wait in seconds for a stalled response before terminating the
connection.  If unspecified, the default is 120 seconds.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>Basic Example:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tenable.dl</span> <span class="kn">import</span> <span class="n">Downloads</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">dl</span> <span class="o">=</span> <span class="n">Downloads</span><span class="p">(</span><span class="n">api_token</span><span class="o">=</span><span class="s1">&#39;API_TOKEN&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>Example with proper identification:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">dl</span> <span class="o">=</span> <span class="n">Downloads</span><span class="p">(</span><span class="s1">&#39;API_TOKEN&#39;</span><span class="p">,</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company Name&#39;</span><span class="p">,</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">product</span><span class="o">=</span><span class="s1">&#39;My Awesome Widget&#39;</span><span class="p">,</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>Example with proper identification leveraging environment variables for
access and secret keys:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">dl</span> <span class="o">=</span> <span class="n">Downloads</span><span class="p">(</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company Name&#39;</span><span class="p">,</span> <span class="n">product</span><span class="o">=</span><span class="s1">&#39;Widget&#39;</span><span class="p">,</span> <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.dl.Downloads.details">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">page</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.dl.Downloads.details" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the specific download items for the page requested.</p>
<p><a class="reference external" href="https://developer.tenable.com/reference/get_pages-slug">API Endpoint Documentation</a></p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>page</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of the page to request.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The page details.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">dict</span></code></a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">details</span> <span class="o">=</span> <span class="n">dl</span><span class="o">.</span><span class="n">details</span><span class="p">(</span><span class="s1">&#39;nessus&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.dl.Downloads.download">
<span class="sig-name descname"><span class="pre">download</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">page</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">package</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">fobj</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads.download"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.dl.Downloads.download" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the requested package and downloads the file.</p>
<p><a class="reference external" href="https://developer.tenable.com/reference/get_pages-slug-files-file">API Endpoint Documentation</a></p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>page</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of the page</p></li>
<li><p><strong>package</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The package filename</p></li>
<li><p><strong>fobj</strong> (<em>FileObject</em><em>, </em><em>optional</em>) – The file-like object to write the package to.  If nothing is
specified, then a BytesIO object will be used.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The binary package</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><code class="xref py py-obj docutils literal notranslate"><span class="pre">FileObject</span></code></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="s1">&#39;Nessus-latest.x86_64.rpm&#39;</span><span class="p">,</span> <span class="s1">&#39;wb&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">pkgfile</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">dl</span><span class="o">.</span><span class="n">download</span><span class="p">(</span><span class="s1">&#39;nessus&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;Nessus-8.3.0-es7.x86_64.rpm&#39;</span><span class="p">,</span> <span class="n">pkgfile</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.dl.Downloads.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.dl.Downloads.list" title="Permalink to this definition">¶</a></dt>
<dd><p>Lists the available content pages.</p>
<p><a class="reference external" href="https://developer.tenable.com/reference/get_pages">API Endpoint Documentation</a></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The list of page resources.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference internal" href="#id3" title="tenable.dl.Downloads.list"><code class="xref py py-obj docutils literal notranslate"><span class="pre">list</span></code></a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">pages</span> <span class="o">=</span> <span class="n">dl</span><span class="o">.</span><span class="n">list</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="k">for</span> <span class="n">page</span> <span class="ow">in</span> <span class="n">pages</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">pprint</span><span class="p">(</span><span class="n">page</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">Downloads</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api_token</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id1" title="tenable.base.platform.APIPlatform"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.platform.APIPlatform</span></code></a></p>
<p>The Downloads object is the primary interaction point for users to
interface with Downloads API via the pyTenable library.  All of the API
endpoint classes that have been written will be grafted onto this class.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>api_token</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The user’s API access key for Tenable.io  If an access key isn’t
specified, then the library will attempt to read the environment
variable <code class="docutils literal notranslate"><span class="pre">TDL_API_TOKEN</span></code> to acquire the key.</p></li>
<li><p><strong>retries</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – The number of retries to make before failing a request.  The
default is <code class="docutils literal notranslate"><span class="pre">5</span></code>.</p></li>
<li><p><strong>backoff</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.10)"><em>float</em></a><em>, </em><em>optional</em>) – If a 429 response is returned, how much do we want to backoff
if the response didn’t send a Retry-After header.  The default
backoff is <code class="docutils literal notranslate"><span class="pre">1</span></code> second.</p></li>
<li><p><strong>vendor</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The vendor name for the User-Agent string.</p></li>
<li><p><strong>product</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The product name for the User-Agent string.</p></li>
<li><p><strong>build</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The version or build identifier for the User-Agent string.</p></li>
<li><p><strong>timeout</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – The connection timeout parameter informing the library how long to
wait in seconds for a stalled response before terminating the
connection.  If unspecified, the default is 120 seconds.</p></li>
</ul>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>Basic Example:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">tenable.dl</span> <span class="kn">import</span> <span class="n">Downloads</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">dl</span> <span class="o">=</span> <span class="n">Downloads</span><span class="p">(</span><span class="n">api_token</span><span class="o">=</span><span class="s1">&#39;API_TOKEN&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>Example with proper identification:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">dl</span> <span class="o">=</span> <span class="n">Downloads</span><span class="p">(</span><span class="s1">&#39;API_TOKEN&#39;</span><span class="p">,</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company Name&#39;</span><span class="p">,</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">product</span><span class="o">=</span><span class="s1">&#39;My Awesome Widget&#39;</span><span class="p">,</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>Example with proper identification leveraging environment variables for
access and secret keys:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">dl</span> <span class="o">=</span> <span class="n">Downloads</span><span class="p">(</span>
<span class="gp">&gt;&gt;&gt; </span>    <span class="n">vendor</span><span class="o">=</span><span class="s1">&#39;Company Name&#39;</span><span class="p">,</span> <span class="n">product</span><span class="o">=</span><span class="s1">&#39;Widget&#39;</span><span class="p">,</span> <span class="n">build</span><span class="o">=</span><span class="s1">&#39;1.0.0&#39;</span><span class="p">)</span>
</pre></div>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">page</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the specific download items for the page requested.</p>
<p><a class="reference external" href="https://developer.tenable.com/reference/get_pages-slug">API Endpoint Documentation</a></p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>page</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of the page to request.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The page details.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">dict</span></code></a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">details</span> <span class="o">=</span> <span class="n">dl</span><span class="o">.</span><span class="n">details</span><span class="p">(</span><span class="s1">&#39;nessus&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id2">
<span class="sig-name descname"><span class="pre">download</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">page</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">package</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">fobj</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads.download"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id2" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the requested package and downloads the file.</p>
<p><a class="reference external" href="https://developer.tenable.com/reference/get_pages-slug-files-file">API Endpoint Documentation</a></p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>page</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of the page</p></li>
<li><p><strong>package</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The package filename</p></li>
<li><p><strong>fobj</strong> (<em>FileObject</em><em>, </em><em>optional</em>) – The file-like object to write the package to.  If nothing is
specified, then a BytesIO object will be used.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The binary package</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><code class="xref py py-obj docutils literal notranslate"><span class="pre">FileObject</span></code></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="s1">&#39;Nessus-latest.x86_64.rpm&#39;</span><span class="p">,</span> <span class="s1">&#39;wb&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">pkgfile</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">dl</span><span class="o">.</span><span class="n">download</span><span class="p">(</span><span class="s1">&#39;nessus&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;Nessus-8.3.0-es7.x86_64.rpm&#39;</span><span class="p">,</span> <span class="n">pkgfile</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id3">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/dl.md#Downloads.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id3" title="Permalink to this definition">¶</a></dt>
<dd><p>Lists the available content pages.</p>
<p><a class="reference external" href="https://developer.tenable.com/reference/get_pages">API Endpoint Documentation</a></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The list of page resources.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference internal" href="#id3" title="tenable.dl.Downloads.list"><code class="xref py py-obj docutils literal notranslate"><span class="pre">list</span></code></a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">pages</span> <span class="o">=</span> <span class="n">dl</span><span class="o">.</span><span class="n">list</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="k">for</span> <span class="n">page</span> <span class="ow">in</span> <span class="n">pages</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">pprint</span><span class="p">(</span><span class="n">page</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
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
          <a href="tenable.io.md" title="tenable.io package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.base.utils.md" title="tenable.base.utils package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.dl package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>