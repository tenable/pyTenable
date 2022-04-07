
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>tenable.base.schema package &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="_static/custom.css" />
    
    <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
    <script src="_static/jquery.js"></script>
    <script src="_static/underscore.js"></script>
    <script src="_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="search" title="Search" href="search.md" />
    <link rel="next" title="tenable.base.utils package" href="tenable.base.utils.md" />
    <link rel="prev" title="tenable.base package" href="tenable.base.md" /> 
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
          <a href="tenable.base.utils.md" title="tenable.base.utils package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.base.md" title="tenable.base package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.base.md" accesskey="U">tenable.base package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.base.schema package</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <section id="module-tenable.base.schema">
<span id="tenable-base-schema-package"></span><h1>tenable.base.schema package<a class="headerlink" href="#module-tenable.base.schema" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.base.schema.fields">
<span id="tenable-base-schema-fields-module"></span><h2>tenable.base.schema.fields module<a class="headerlink" href="#module-tenable.base.schema.fields" title="Permalink to this headline">¶</a></h2>
<p>Extended field definitions</p>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.base.schema.fields.BaseField">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">BaseField</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">inner</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/schema/fields.md#BaseField"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.schema.fields.BaseField" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">marshmallow.fields.Field</span></code></p>
<p>BaseField Field</p>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="tenable.base.schema.fields.LowerCase">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">LowerCase</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">inner</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/schema/fields.md#LowerCase"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.schema.fields.LowerCase" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="#tenable.base.schema.fields.BaseField" title="tenable.base.schema.fields.BaseField"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.schema.fields.BaseField</span></code></a></p>
<p>The field value will be lower-cased with this field.</p>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="tenable.base.schema.fields.UpperCase">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">UpperCase</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">inner</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/base/schema/fields.md#UpperCase"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.base.schema.fields.UpperCase" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="#tenable.base.schema.fields.BaseField" title="tenable.base.schema.fields.BaseField"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.schema.fields.BaseField</span></code></a></p>
<p>The field value will be upper-cased with this field.</p>
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
          <a href="tenable.base.utils.md" title="tenable.base.utils package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.base.md" title="tenable.base package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.base.md" >tenable.base package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.base.schema package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>