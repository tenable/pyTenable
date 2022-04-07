
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>tenable.base.utils package &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="_static/custom.css" />
    
    <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
    <script src="_static/jquery.js"></script>
    <script src="_static/underscore.js"></script>
    <script src="_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="search" title="Search" href="search.md" />
    <link rel="next" title="tenable.dl package" href="tenable.dl.md" />
    <link rel="prev" title="tenable.base.schema package" href="tenable.base.schema.md" /> 
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
          <a href="tenable.dl.md" title="tenable.dl package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.base.schema.md" title="tenable.base.schema package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.base.md" accesskey="U">tenable.base package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.base.utils package</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <section id="module-tenable.base.utils">
<span id="tenable-base-utils-package"></span><h1>tenable.base.utils package<a class="headerlink" href="#module-tenable.base.utils" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.base.utils.envelope">
<span id="tenable-base-utils-envelope-module"></span><h2>tenable.base.utils.envelope module<a class="headerlink" href="#module-tenable.base.utils.envelope" title="Permalink to this headline">¶</a></h2>
<p>Dictionary enveloping utility.</p>
<dl class="py function">
<dt class="sig sig-object py" id="tenable.base.utils.envelope.envelope">
<span class="sig-name descname"><span class="pre">envelope</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">excludes</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/base/utils/envelope.md#envelope"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.utils.envelope.envelope" title="Permalink to this definition">¶</a></dt>
<dd><p>Reformats the data dictionary to push any keys that aren’t described in the
excludes list into the filters sub-object.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>data</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – The data dictionary to modify</p></li>
<li><p><strong>key</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The dictionary key to wrap the data within.</p></li>
<li><p><strong>excludes</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)"><em>list</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>]</em><em>, </em><em>optional</em>) – A list of keys to exclude from the enveloping process.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The modified data dictionary.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
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
          <a href="tenable.dl.md" title="tenable.dl package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.base.schema.md" title="tenable.base.schema package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.base.md" >tenable.base package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.base.utils package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>