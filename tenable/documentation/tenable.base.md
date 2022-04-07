<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="next" title="tenable.base.schema package" href="tenable.base.schema.md" />
    <link rel="prev" title="tenable.ad.widget package" href="tenable.ad.widget.md" /> 
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
          <a href="tenable.base.schema.md" title="tenable.base.schema package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.widget.md" title="tenable.ad.widget package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.base package</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <section id="module-tenable.base">
<span id="tenable-base-package"></span><h1>tenable.base package<a class="headerlink" href="#module-tenable.base" title="Permalink to this headline">¶</a></h1>
<section id="subpackages">
<h2>Subpackages<a class="headerlink" href="#subpackages" title="Permalink to this headline">¶</a></h2>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="tenable.base.schema.md">tenable.base.schema package</a><ul>
<li class="toctree-l2"><a class="reference internal" href="tenable.base.schema.md#submodules">Submodules</a></li>
<li class="toctree-l2"><a class="reference internal" href="tenable.base.schema.md#module-tenable.base.schema.fields">tenable.base.schema.fields module</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="tenable.base.utils.md">tenable.base.utils package</a><ul>
<li class="toctree-l2"><a class="reference internal" href="tenable.base.utils.md#submodules">Submodules</a></li>
<li class="toctree-l2"><a class="reference internal" href="tenable.base.utils.md#module-tenable.base.utils.envelope">tenable.base.utils.envelope module</a></li>
</ul>
</li>
</ul>
</div>
</section>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.base.endpoint">
<span id="tenable-base-endpoint-module"></span><h2>tenable.base.endpoint module<a class="headerlink" href="#module-tenable.base.endpoint" title="Permalink to this headline">¶</a></h2>
<section id="base-endpoint">
<h3>Base Endpoint<a class="headerlink" href="#base-endpoint" title="Permalink to this headline">¶</a></h3>
<p>The APIEndpoint class is the base class that all endpoint modules will inherit
from.  Throughout pyTenable v1, packages will be transitioning to using this
base class over the original APISession class.</p>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.base.endpoint.APIEndpoint">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">APIEndpoint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/endpoint.md#APIEndpoint"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.endpoint.APIEndpoint" title="Permalink to this definition">¶</a></dt>
<dd><p>Base API Endpoint class</p>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">APIEndpoint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/endpoint.md#APIEndpoint"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/endpoint.html#restfly.endpoint.APIEndpoint" title="(in RESTfly v1.4.6)"><code class="xref py py-class docutils literal notranslate"><span class="pre">restfly.endpoint.APIEndpoint</span></code></a></p>
<p>Base API Endpoint class</p>
</dd></dl>
</section>
</section>
<section id="module-tenable.base.platform">
<span id="tenable-base-platform-module"></span><h2>tenable.base.platform module<a class="headerlink" href="#module-tenable.base.platform" title="Permalink to this headline">¶</a></h2>
<section id="base-platform">
<h3>Base Platform<a class="headerlink" href="#base-platform" title="Permalink to this headline">¶</a></h3>
<p>The APIPlatform class is the base class that all platform packages will inherit
from.  Throughout pyTenable v1, packages will be transitioning to using this
base class over the original APISession class.</p>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.base.platform.APIPlatform">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">APIPlatform</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/platform.md#APIPlatform"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.platform.APIPlatform" title="Permalink to this definition">¶</a></dt>
<dd><p>Base class for all API Platform packages.  This class handles all of the
base connection logic.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>adaptor</strong> (<em>Object</em><em>, </em><em>optional</em>) – A Requests Session adaptor to bind to the session object.</p></li>
<li><p><strong>backoff</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.10)"><em>float</em></a><em>, </em><em>optional</em>) – If a 429 response is returned, how much do we want to backoff
if the response didn’t send a Retry-After header.  If left
unspecified, the default is 1 second.</p></li>
<li><p><strong>box</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a><em>, </em><em>optional</em>) – Should responses be passed through Box?  If left unspecified, the
default is <code class="docutils literal notranslate"><span class="pre">True</span></code>.</p></li>
<li><p><strong>box_attrs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – Any additional attributes to pass to the Box constructor for this
session?  For a list of attributes that can be sent, please refer
to the
<a class="reference external" href="https://github.com/cdgriffith/Box/wiki">Box documentation</a>
for more information.</p></li>
<li><p><strong>build</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The build number to put into the User-Agent string.</p></li>
<li><p><strong>product</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The product name to put into the User-Agent string.</p></li>
<li><p><strong>proxies</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – A dictionary detailing what proxy should be used for what
transport protocol.  This value will be passed to the session
object after it has been either attached or created.  For
details on the structure of this dictionary, consult the
<a class="reference external" href="https://requests.readthedocs.io/en/master/user/advanced/#proxies">proxies</a> section of the
Requests documentation.</p></li>
<li><p><strong>retries</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – The number of retries to make before failing a request.  The
default is 5.</p></li>
<li><p><strong>session</strong> (<a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Session" title="(in Requests v2.26.0)"><em>requests.Session</em></a><em>, </em><em>optional</em>) – Provide a pre-built session instead of creating a requests
session at instantiation.</p></li>
<li><p><strong>squash_camel</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a><em>, </em><em>optional</em>) – Should the responses have CamelCase responses be squashed into
snake_case?  If left unspecified, the default value is <code class="docutils literal notranslate"><span class="pre">False</span></code>.
Note that this will only work when Box is enabled.</p></li>
<li><p><strong>ssl_verify</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a><em>, </em><em>optional</em>) – If SSL Verification needs to be disabled (for example when using
a self-signed certificate), then this parameter should be set to
<code class="docutils literal notranslate"><span class="pre">False</span></code> to disable verification and mask the Certificate
warnings.</p></li>
<li><p><strong>url</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The base URL that the paths will be appended onto.</p></li>
<li><p><strong>vendor</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The vendor name to put into the User-Agent string.</p></li>
</ul>
</dd>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.base.platform.APIPlatform.delete">
<span class="sig-name descname"><span class="pre">delete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><span class="pre">box.box.Box</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">box.box_list.BoxList</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">requests.models.Response</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#tenable.base.platform.APIPlatform.delete" title="Permalink to this definition">¶</a></dt>
<dd><p>Initiates an HTTP DELETE request using the specified path.  Refer to
the <a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.request" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.request</span></code></a> for more detailed information on what
keyword arguments can be passed:</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The path to be appended onto the base URL for the request.</p></li>
<li><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – Keyword arguments to be passed to
<a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession._req" title="(in RESTfly v1.4.6)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">restfly.session.APISession._req()</span></code></a>.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><dl class="simple">
<dt><a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Response" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.Response</span></code></a> or <code class="xref py py-obj docutils literal notranslate"><span class="pre">box.Box</span></code></dt><dd><p>If the request was informed to attempt to “boxify” the response
and the response was JSON data, then a Box will be returned.
In all other scenarios, a Response object will be returned.</p>
</dd>
</dl>
</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">api</span> <span class="o">=</span> <span class="n">APISession</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">resp</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;/&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.base.platform.APIPlatform.get">
<span class="sig-name descname"><span class="pre">get</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><span class="pre">box.box.Box</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">box.box_list.BoxList</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">requests.models.Response</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#tenable.base.platform.APIPlatform.get" title="Permalink to this definition">¶</a></dt>
<dd><p>Initiates an HTTP GET request using the specified path.  Refer to
<a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.request" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.request</span></code></a> for more detailed information on what
keyword arguments can be passed:</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The path to be appended onto the base URL for the request.</p></li>
<li><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – Keyword arguments to be passed to
<a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession._req" title="(in RESTfly v1.4.6)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">restfly.session.APISession._req()</span></code></a>.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><dl class="simple">
<dt><a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Response" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.Response</span></code></a> or <code class="xref py py-obj docutils literal notranslate"><span class="pre">box.Box</span></code></dt><dd><p>If the request was informed to attempt to “boxify” the response
and the response was JSON data, then a Box will be returned.
In all other scenarios, a Response object will be returned.</p>
</dd>
</dl>
</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">api</span> <span class="o">=</span> <span class="n">APISession</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">resp</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;/&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.base.platform.APIPlatform.head">
<span class="sig-name descname"><span class="pre">head</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><span class="pre">box.box.Box</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">box.box_list.BoxList</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">requests.models.Response</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#tenable.base.platform.APIPlatform.head" title="Permalink to this definition">¶</a></dt>
<dd><p>Initiates an HTTP HEAD request using the specified path.  Refer to the
<a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.request" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.request</span></code></a> for more detailed information on what
keyword arguments can be passed:</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The path to be appended onto the base URL for the request.</p></li>
<li><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – Keyword arguments to be passed to
<a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession._req" title="(in RESTfly v1.4.6)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">restfly.session.APISession._req()</span></code></a>.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><dl class="simple">
<dt><a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Response" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.Response</span></code></a> or <code class="xref py py-obj docutils literal notranslate"><span class="pre">box.Box</span></code></dt><dd><p>If the request was informed to attempt to “boxify” the response
and the response was JSON data, then a Box will be returned.
In all other scenarios, a Response object will be returned.</p>
</dd>
</dl>
</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">api</span> <span class="o">=</span> <span class="n">APISession</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">resp</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">head</span><span class="p">(</span><span class="s1">&#39;/&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.base.platform.APIPlatform.patch">
<span class="sig-name descname"><span class="pre">patch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><span class="pre">box.box.Box</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">box.box_list.BoxList</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">requests.models.Response</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#tenable.base.platform.APIPlatform.patch" title="Permalink to this definition">¶</a></dt>
<dd><p>Initiates an HTTP PATCH request using the specified path.  Refer to the
<a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.request" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.request</span></code></a> for more detailed information on what
keyword arguments can be passed:</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The path to be appended onto the base URL for the request.</p></li>
<li><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – Keyword arguments to be passed to
<a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession._req" title="(in RESTfly v1.4.6)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">restfly.session.APISession._req()</span></code></a>.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><dl class="simple">
<dt><a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Response" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.Response</span></code></a> or <code class="xref py py-obj docutils literal notranslate"><span class="pre">box.Box</span></code></dt><dd><p>If the request was informed to attempt to “boxify” the response
and the response was JSON data, then a Box will be returned.
In all other scenarios, a Response object will be returned.</p>
</dd>
</dl>
</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">api</span> <span class="o">=</span> <span class="n">APISession</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">resp</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;/&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.base.platform.APIPlatform.post">
<span class="sig-name descname"><span class="pre">post</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><span class="pre">box.box.Box</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">box.box_list.BoxList</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">requests.models.Response</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#tenable.base.platform.APIPlatform.post" title="Permalink to this definition">¶</a></dt>
<dd><p>Initiates an HTTP POST request using the specified path.  Refer to the
<a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.request" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.request</span></code></a> for more detailed information on what
keyword arguments can be passed:</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The path to be appended onto the base URL for the request.</p></li>
<li><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – Keyword arguments to be passed to
<a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession._req" title="(in RESTfly v1.4.6)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">restfly.session.APISession._req()</span></code></a>.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><dl class="simple">
<dt><a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Response" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.Response</span></code></a> or <code class="xref py py-obj docutils literal notranslate"><span class="pre">box.Box</span></code></dt><dd><p>If the request was informed to attempt to “boxify” the response
and the response was JSON data, then a Box will be returned.
In all other scenarios, a Response object will be returned.</p>
</dd>
</dl>
</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">api</span> <span class="o">=</span> <span class="n">APISession</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">resp</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;/&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.base.platform.APIPlatform.put">
<span class="sig-name descname"><span class="pre">put</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><span class="pre">box.box.Box</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">box.box_list.BoxList</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">requests.models.Response</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#tenable.base.platform.APIPlatform.put" title="Permalink to this definition">¶</a></dt>
<dd><p>Initiates an HTTP PUT request using the specified path.  Refer to the
<a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.request" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.request</span></code></a> for more detailed information on what
keyword arguments can be passed:</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The path to be appended onto the base URL for the request.</p></li>
<li><p><strong>**kwargs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – Keyword arguments to be passed to
<a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession._req" title="(in RESTfly v1.4.6)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">restfly.session.APISession._req()</span></code></a>.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><dl class="simple">
<dt><a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Response" title="(in Requests v2.26.0)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">requests.Response</span></code></a> or <code class="xref py py-obj docutils literal notranslate"><span class="pre">box.Box</span></code></dt><dd><p>If the request was informed to attempt to “boxify” the response
and the response was JSON data, then a Box will be returned.
In all other scenarios, a Response object will be returned.</p>
</dd>
</dl>
</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">api</span> <span class="o">=</span> <span class="n">APISession</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">resp</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">put</span><span class="p">(</span><span class="s1">&#39;/&#39;</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id1">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">APIPlatform</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/platform.md#APIPlatform"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><code class="xref py py-class docutils literal notranslate"><span class="pre">restfly.session.APISession</span></code></a></p>
<p>Base class for all API Platform packages.  This class handles all of the
base connection logic.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>adaptor</strong> (<em>Object</em><em>, </em><em>optional</em>) – A Requests Session adaptor to bind to the session object.</p></li>
<li><p><strong>backoff</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.10)"><em>float</em></a><em>, </em><em>optional</em>) – If a 429 response is returned, how much do we want to backoff
if the response didn’t send a Retry-After header.  If left
unspecified, the default is 1 second.</p></li>
<li><p><strong>box</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a><em>, </em><em>optional</em>) – Should responses be passed through Box?  If left unspecified, the
default is <code class="docutils literal notranslate"><span class="pre">True</span></code>.</p></li>
<li><p><strong>box_attrs</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – <p>Any additional attributes to pass to the Box constructor for this
session?  For a list of attributes that can be sent, please refer
to the
<a class="reference external" href="https://github.com/cdgriffith/Box/wiki">Box documentation</a>
for more information.</p>
</p></li>
<li><p><strong>build</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The build number to put into the User-Agent string.</p></li>
<li><p><strong>product</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The product name to put into the User-Agent string.</p></li>
<li><p><strong>proxies</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a><em>, </em><em>optional</em>) – A dictionary detailing what proxy should be used for what
transport protocol.  This value will be passed to the session
object after it has been either attached or created.  For
details on the structure of this dictionary, consult the
<a class="reference external" href="https://requests.readthedocs.io/en/master/user/advanced/#proxies">proxies</a> section of the
Requests documentation.</p></li>
<li><p><strong>retries</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>, </em><em>optional</em>) – The number of retries to make before failing a request.  The
default is 5.</p></li>
<li><p><strong>session</strong> (<a class="reference external" href="https://docs.python-requests.org/en/master/api/#requests.Session" title="(in Requests v2.26.0)"><em>requests.Session</em></a><em>, </em><em>optional</em>) – Provide a pre-built session instead of creating a requests
session at instantiation.</p></li>
<li><p><strong>squash_camel</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a><em>, </em><em>optional</em>) – Should the responses have CamelCase responses be squashed into
snake_case?  If left unspecified, the default value is <code class="docutils literal notranslate"><span class="pre">False</span></code>.
Note that this will only work when Box is enabled.</p></li>
<li><p><strong>ssl_verify</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a><em>, </em><em>optional</em>) – If SSL Verification needs to be disabled (for example when using
a self-signed certificate), then this parameter should be set to
<code class="docutils literal notranslate"><span class="pre">False</span></code> to disable verification and mask the Certificate
warnings.</p></li>
<li><p><strong>url</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The base URL that the paths will be appended onto.</p></li>
<li><p><strong>vendor</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>, </em><em>optional</em>) – The vendor name to put into the User-Agent string.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
</section>
</section>
<section id="module-tenable.base.v1">
<span id="tenable-base-v1-module"></span><h2>tenable.base.v1 module<a class="headerlink" href="#module-tenable.base.v1" title="Permalink to this headline">¶</a></h2>
<section id="version-1-base-classes">
<h3>Version 1 Base Classes<a class="headerlink" href="#version-1-base-classes" title="Permalink to this headline">¶</a></h3>
<p>These classes are what pyTenable &lt; 1.2 used for all interactions.  They are here
as most of the library will still use it until these have been phased out in
favor of the newer RESTfly-derived classes.</p>
<p>As these classes exist only as a basis for the application packages, it isn’t
recommended to use this directly.  Further if you’re looking for a generic API
interface to use for your own uses, take a look at the RESTfly library.</p>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.base.v1.APIResultsIterator">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">APIResultsIterator</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/v1.md#APIResultsIterator"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.v1.APIResultsIterator" title="Permalink to this definition">¶</a></dt>
<dd><p>The API iterator provides a scalable way to work through result sets of any
size.  The iterator will walk through each page of data, returning one
record at a time.  If it reaches the end of a page of records, then it will
request the next page of information and then continue to return records
from the next page (and the next, and the next) until the counter reaches
the total number of records that the API has reported.</p>
<p>Note that this Iterator is used as a base model for all of the iterators,
and while the mechanics of each iterator may vary, they should all behave
to the user in a similar manner.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>count</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The current number of records that have been returned</p></li>
<li><p><strong>page</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)"><em>list</em></a>) – The current page of data being walked through.  pages will be
cycled through as the iterator requests more information from the
API.</p></li>
<li><p><strong>page_count</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The number of record returned from the current page.</p></li>
<li><p><strong>total</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The total number of records that exist for the current request.</p></li>
</ul>
</dd>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.base.v1.APIResultsIterator.next">
<span class="sig-name descname"><span class="pre">next</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/v1.md#APIResultsIterator.next"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.v1.APIResultsIterator.next" title="Permalink to this definition">¶</a></dt>
<dd><p>Ask for the next record</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id3">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">APIResultsIterator</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/v1.md#APIResultsIterator"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id3" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference external" href="https://docs.python.org/3/library/functions.html#object" title="(in Python v3.10)"><code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></a></p>
<p>The API iterator provides a scalable way to work through result sets of any
size.  The iterator will walk through each page of data, returning one
record at a time.  If it reaches the end of a page of records, then it will
request the next page of information and then continue to return records
from the next page (and the next, and the next) until the counter reaches
the total number of records that the API has reported.</p>
<p>Note that this Iterator is used as a base model for all of the iterators,
and while the mechanics of each iterator may vary, they should all behave
to the user in a similar manner.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>count</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The current number of records that have been returned</p></li>
<li><p><strong>page</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)"><em>list</em></a>) – The current page of data being walked through.  pages will be
cycled through as the iterator requests more information from the
API.</p></li>
<li><p><strong>page_count</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The number of record returned from the current page.</p></li>
<li><p><strong>total</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The total number of records that exist for the current request.</p></li>
</ul>
</dd>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="id4">
<span class="sig-name descname"><span class="pre">next</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/v1.md#APIResultsIterator.next"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id4" title="Permalink to this definition">¶</a></dt>
<dd><p>Ask for the next record</p>
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
          <a href="tenable.base.schema.md" title="tenable.base.schema package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.widget.md" title="tenable.ad.widget package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.base package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>