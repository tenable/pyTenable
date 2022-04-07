
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>tenable.ad.checker_option package &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="_static/custom.css" />
    
    <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
    <script src="_static/jquery.js"></script>
    <script src="_static/underscore.js"></script>
    <script src="_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="search" title="Search" href="search.md" />
    <link rel="next" title="tenable.ad.dashboard package" href="tenable.ad.dashboard.md" />
    <link rel="prev" title="tenable.ad.checker package" href="tenable.ad.checker.md" /> 
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
          <a href="tenable.ad.dashboard.md" title="tenable.ad.dashboard package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.checker.md" title="tenable.ad.checker package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" accesskey="U">tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker_option package</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <section id="module-tenable.ad.checker_option">
<span id="tenable-ad-checker-option-package"></span><h1>tenable.ad.checker_option package<a class="headerlink" href="#module-tenable.ad.checker_option" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.ad.checker_option.api">
<span id="tenable-ad-checker-option-api-module"></span><h2>tenable.ad.checker_option.api module<a class="headerlink" href="#module-tenable.ad.checker_option.api" title="Permalink to this headline">¶</a></h2>
<section id="checker-option">
<h3>Checker Option<a class="headerlink" href="#checker-option" title="Permalink to this headline">¶</a></h3>
<p>Methods described in this section relate to the the checker option API.
These methods can be accessed at <code class="docutils literal notranslate"><span class="pre">TenableAD.checker_option</span></code>.</p>
<dl class="py class hide-signature">
<dt class="sig sig-object py" id="tenable.ad.checker_option.api.CheckerOptionAPI">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">CheckerOptionAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/checker_option/api.md#CheckerOptionAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.checker_option.api.CheckerOptionAPI" title="Permalink to this definition">¶</a></dt>
<dd><dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.checker_option.api.CheckerOptionAPI.create">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">profile_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">checker_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/checker_option/api.md#CheckerOptionAPI.create"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.checker_option.api.CheckerOptionAPI.create" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates the new checker-option.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>profile_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The profile instance identifier.</p></li>
<li><p><strong>checker_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The checker instance identifier.</p></li>
<li><p><strong>codename</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The codename of the checker option.</p></li>
<li><p><strong>value</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The value of the checker option.</p></li>
<li><p><strong>value_type</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The type of the checker option. Accepted values are:
<code class="docutils literal notranslate"><span class="pre">string</span></code>, <code class="docutils literal notranslate"><span class="pre">regex</span></code>, <code class="docutils literal notranslate"><span class="pre">float</span></code>, <code class="docutils literal notranslate"><span class="pre">integer</span></code>, <code class="docutils literal notranslate"><span class="pre">boolean</span></code>,
<code class="docutils literal notranslate"><span class="pre">date</span></code>, <code class="docutils literal notranslate"><span class="pre">object</span></code>, <code class="docutils literal notranslate"><span class="pre">array/string</span></code>, <code class="docutils literal notranslate"><span class="pre">array/regex</span></code>,
<code class="docutils literal notranslate"><span class="pre">array/integer</span></code>, <code class="docutils literal notranslate"><span class="pre">array/boolean</span></code>, <code class="docutils literal notranslate"><span class="pre">array/select</span></code>,
<code class="docutils literal notranslate"><span class="pre">array/object</span></code>.</p></li>
<li><p><strong>directory_id</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The directory instance identifier.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>Created checker option instance.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">checker_option</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;9&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">checker_id</span><span class="o">=</span><span class="s1">&#39;2&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">codename</span><span class="o">=</span><span class="s1">&#39;codename&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">value</span><span class="o">=</span><span class="s1">&#39;false&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">value_type</span><span class="o">=</span><span class="s1">&#39;boolean&#39;</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="mi">3</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.checker_option.api.CheckerOptionAPI.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">profile_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">checker_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/checker_option/api.md#CheckerOptionAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.checker_option.api.CheckerOptionAPI.list" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the list of checker-options.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>profile_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The profile instance identifier.</p></li>
<li><p><strong>checker_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The checker instance identifier.</p></li>
<li><p><strong>staged</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a>) – Get only the checker-options that are staged. Accepted
values are <code class="docutils literal notranslate"><span class="pre">True</span></code> and <code class="docutils literal notranslate"><span class="pre">False</span></code>. Added checker options
are first staged until the profile is commited. The staged
profile options are not activated and don’t affect
yet the IOE and the exposure detection.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>List of checker options.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">checker_option</span><span class="o">.</span><span class="n">list</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;9&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">checker_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">staged</span><span class="o">=</span><span class="kc">True</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">CheckerOptionAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/checker_option/api.md#CheckerOptionAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id0" title="tenable.base.endpoint.APIEndpoint"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.endpoint.APIEndpoint</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">profile_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">checker_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/checker_option/api.md#CheckerOptionAPI.create"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates the new checker-option.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>profile_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The profile instance identifier.</p></li>
<li><p><strong>checker_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The checker instance identifier.</p></li>
<li><p><strong>codename</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The codename of the checker option.</p></li>
<li><p><strong>value</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The value of the checker option.</p></li>
<li><p><strong>value_type</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The type of the checker option. Accepted values are:
<code class="docutils literal notranslate"><span class="pre">string</span></code>, <code class="docutils literal notranslate"><span class="pre">regex</span></code>, <code class="docutils literal notranslate"><span class="pre">float</span></code>, <code class="docutils literal notranslate"><span class="pre">integer</span></code>, <code class="docutils literal notranslate"><span class="pre">boolean</span></code>,
<code class="docutils literal notranslate"><span class="pre">date</span></code>, <code class="docutils literal notranslate"><span class="pre">object</span></code>, <code class="docutils literal notranslate"><span class="pre">array/string</span></code>, <code class="docutils literal notranslate"><span class="pre">array/regex</span></code>,
<code class="docutils literal notranslate"><span class="pre">array/integer</span></code>, <code class="docutils literal notranslate"><span class="pre">array/boolean</span></code>, <code class="docutils literal notranslate"><span class="pre">array/select</span></code>,
<code class="docutils literal notranslate"><span class="pre">array/object</span></code>.</p></li>
<li><p><strong>directory_id</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The directory instance identifier.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>Created checker option instance.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">checker_option</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;9&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">checker_id</span><span class="o">=</span><span class="s1">&#39;2&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">codename</span><span class="o">=</span><span class="s1">&#39;codename&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">value</span><span class="o">=</span><span class="s1">&#39;false&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">value_type</span><span class="o">=</span><span class="s1">&#39;boolean&#39;</span>
<span class="gp">... </span>    <span class="n">directory_id</span><span class="o">=</span><span class="mi">3</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="id2">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">profile_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">checker_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/checker_option/api.md#CheckerOptionAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id2" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the list of checker-options.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>profile_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The profile instance identifier.</p></li>
<li><p><strong>checker_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The checker instance identifier.</p></li>
<li><p><strong>staged</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a>) – Get only the checker-options that are staged. Accepted
values are <code class="docutils literal notranslate"><span class="pre">True</span></code> and <code class="docutils literal notranslate"><span class="pre">False</span></code>. Added checker options
are first staged until the profile is commited. The staged
profile options are not activated and don’t affect
yet the IOE and the exposure detection.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>List of checker options.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">checker_option</span><span class="o">.</span><span class="n">list</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;9&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">checker_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">staged</span><span class="o">=</span><span class="kc">True</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>

</dd></dl>

</section>
</section>
<section id="module-tenable.ad.checker_option.schema">
<span id="tenable-ad-checker-option-schema-module"></span><h2>tenable.ad.checker_option.schema module<a class="headerlink" href="#module-tenable.ad.checker_option.schema" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.checker_option.schema.CheckerOptionSchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">CheckerOptionSchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/checker_option/schema.md#CheckerOptionSchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.checker_option.schema.CheckerOptionSchema" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.ad.base.md#tenable.ad.base.schema.CamelCaseSchema" title="tenable.ad.base.schema.CamelCaseSchema"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.ad.base.schema.CamelCaseSchema</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.checker_option.schema.CheckerOptionSchema.keys_to_camel">
<span class="sig-name descname"><span class="pre">keys_to_camel</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/checker_option/schema.md#CheckerOptionSchema.keys_to_camel"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.checker_option.schema.CheckerOptionSchema.keys_to_camel" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

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
          <a href="tenable.ad.dashboard.md" title="tenable.ad.dashboard package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.checker.md" title="tenable.ad.checker package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" >tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker_option package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>