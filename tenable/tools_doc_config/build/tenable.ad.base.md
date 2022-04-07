
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>tenable.ad.base package &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="_static/custom.css" />
    
    <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
    <script src="_static/jquery.js"></script>
    <script src="_static/underscore.js"></script>
    <script src="_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="search" title="Search" href="search.md" />
    <link rel="next" title="tenable.ad.category package" href="tenable.ad.category.md" />
    <link rel="prev" title="tenable.ad.attack_types package" href="tenable.ad.attack_types.md" /> 
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
          <a href="tenable.ad.category.md" title="tenable.ad.category package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.attack_types.md" title="tenable.ad.attack_types package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" accesskey="U">tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.base package</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <section id="module-tenable.ad.base">
<span id="tenable-ad-base-package"></span><h1>tenable.ad.base package<a class="headerlink" href="#module-tenable.ad.base" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.ad.base.schema">
<span id="tenable-ad-base-schema-module"></span><h2>tenable.ad.base.schema module<a class="headerlink" href="#module-tenable.ad.base.schema" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.base.schema.BoolInt">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">BoolInt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">truthy</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.10)"><span class="pre">set</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">falsy</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.10)"><span class="pre">set</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/base/schema.md#BoolInt"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.base.schema.BoolInt" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">marshmallow.fields.Boolean</span></code></p>
<p>Schema to return an integer value for given boolean value</p>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.base.schema.CamelCaseSchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">CamelCaseSchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/base/schema.md#CamelCaseSchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.base.schema.CamelCaseSchema" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">marshmallow.schema.Schema</span></code></p>
<p>Schema that uses camel-case for its external representation
and snake-case for its internal representation.</p>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.base.schema.CamelCaseSchema.on_bind_field">
<span class="sig-name descname"><span class="pre">on_bind_field</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">field_name</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">field_obj</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/base/schema.md#CamelCaseSchema.on_bind_field"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.base.schema.CamelCaseSchema.on_bind_field" title="Permalink to this definition">¶</a></dt>
<dd><p>Hook to modify a field when it is bound to the <cite>Schema</cite>.</p>
<p>No-op by default.</p>
</dd></dl>

</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="tenable.ad.base.schema.camelcase">
<span class="sig-name descname"><span class="pre">camelcase</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">s</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/base/schema.md#camelcase"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.base.schema.camelcase" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="tenable.ad.base.schema.convert_keys_to_camel">
<span class="sig-name descname"><span class="pre">convert_keys_to_camel</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">special</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/base/schema.md#convert_keys_to_camel"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.base.schema.convert_keys_to_camel" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert dictionary keys to camel case</p>
<p class="rubric">Example</p>
<p>example_field -&gt; exampleField</p>
<p>and for special field names
will convert last word to uppercase.</p>
<p class="rubric">Example</p>
<p>example_field -&gt; exampleFIELD</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>data</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><em>dict</em></a>) – The data dictionary.</p></li>
<li><p><strong>special</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)"><em>list</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a><em>]</em>) – The list of special field for converting last word to uppercase.</p></li>
</ul>
</dd>
</dl>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="tenable.ad.base.schema.last_word_uppercase">
<span class="sig-name descname"><span class="pre">last_word_uppercase</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">s</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/base/schema.md#last_word_uppercase"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.base.schema.last_word_uppercase" title="Permalink to this definition">¶</a></dt>
<dd><p>converts last word to uppercase</p>
<p class="rubric">Example</p>
<p>example_field -&gt; exampleFIELD</p>
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
          <a href="tenable.ad.category.md" title="tenable.ad.category package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.attack_types.md" title="tenable.ad.attack_types package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" >tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.base package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>