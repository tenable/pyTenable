
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>tenable.reports package &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="_static/custom.css" />
    
    <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
    <script src="_static/jquery.js"></script>
    <script src="_static/underscore.js"></script>
    <script src="_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="search" title="Search" href="search.md" />
    <link rel="next" title="tenable.sc package" href="tenable.sc.md" />
    <link rel="prev" title="tenable.ot.graphql package" href="tenable.ot.graphql.md" /> 
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
          <a href="tenable.sc.md" title="tenable.sc package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ot.graphql.md" title="tenable.ot.graphql package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.reports package</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <section id="module-tenable.reports">
<span id="tenable-reports-package"></span><h1>tenable.reports package<a class="headerlink" href="#module-tenable.reports" title="Permalink to this headline">¶</a></h1>
<section id="understanding-tenable-report-formats">
<h2>Understanding Tenable Report Formats<a class="headerlink" href="#understanding-tenable-report-formats" title="Permalink to this headline">¶</a></h2>
<p>Nessus, SecurityCenter, Tenable.io, and other Tenable applications produce data
in several formats.  While most of these formats are meant to be consumable by
the user directly (such as PDF, CSV, and HTML reports), some of these formats
are meant to be used for machine to machine transfers.  The most notable example
of this is the Nessus version 2 file format.</p>
<p>The Nessus version 2 format is a XML-based format that allows for a wide range
of flexibility in providing different and varied sets of data within a singular
report.  While not very data dense (reports can get quite large in size), it’s
easily compressible and well understood.</p>
<span class="target" id="module-tenable.reports.nessusv2"></span><dl class="py class">
<dt class="sig sig-object py" id="tenable.reports.nessusv2.NessusReportv2">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">NessusReportv2</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fobj</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/reports/nessusv2.md#NessusReportv2"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.reports.nessusv2.NessusReportv2" title="Permalink to this definition">¶</a></dt>
<dd><p>The NessusReportv2 generator will return vulnerability items from any
Nessus version 2 formatted Nessus report file.  The returned data will be
a python dictionary representation of the ReportItem with the relevant
host properties attached.  The ReportItem’s structure itself will determine
the resulting dictionary, what attributes are returned, and what is not.</p>
<p>Please note that in order to use this generator, you must install the python
<code class="docutils literal notranslate"><span class="pre">lxml</span></code> package.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>fobj</strong> (<em>File object</em><em> or </em><em>string path</em>) – Either a File-like object or a string path pointing to the file to
be parsed.</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>For example, if we wanted to load a Nessus report from disk and iterate
through the contents, it would simply be a matter of:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="s1">&#39;example.nessus&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">nessus_file</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">report</span> <span class="o">=</span> <span class="n">NessusReportv2</span><span class="p">(</span><span class="n">nessus_file</span><span class="p">)</span>
<span class="gp">... </span>    <span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">report</span><span class="p">:</span>
<span class="gp">... </span>        <span class="nb">print</span><span class="p">(</span><span class="n">item</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>

</section>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-0">
<span id="tenable-reports-nessusv2-module"></span><h2>tenable.reports.nessusv2 module<a class="headerlink" href="#module-0" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">NessusReportv2</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fobj</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/reports/nessusv2.md#NessusReportv2"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>The NessusReportv2 generator will return vulnerability items from any
Nessus version 2 formatted Nessus report file.  The returned data will be
a python dictionary representation of the ReportItem with the relevant
host properties attached.  The ReportItem’s structure itself will determine
the resulting dictionary, what attributes are returned, and what is not.</p>
<p>Please note that in order to use this generator, you must install the python
<code class="docutils literal notranslate"><span class="pre">lxml</span></code> package.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>fobj</strong> (<em>File object</em><em> or </em><em>string path</em>) – Either a File-like object or a string path pointing to the file to
be parsed.</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>For example, if we wanted to load a Nessus report from disk and iterate
through the contents, it would simply be a matter of:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="s1">&#39;example.nessus&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">nessus_file</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">report</span> <span class="o">=</span> <span class="n">NessusReportv2</span><span class="p">(</span><span class="n">nessus_file</span><span class="p">)</span>
<span class="gp">... </span>    <span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">report</span><span class="p">:</span>
<span class="gp">... </span>        <span class="nb">print</span><span class="p">(</span><span class="n">item</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="id1">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">NessusReportv2</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fobj</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/reports/nessusv2.md#NessusReportv2"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference external" href="https://docs.python.org/3/library/functions.html#object" title="(in Python v3.10)"><code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></a></p>
<p>The NessusReportv2 generator will return vulnerability items from any
Nessus version 2 formatted Nessus report file.  The returned data will be
a python dictionary representation of the ReportItem with the relevant
host properties attached.  The ReportItem’s structure itself will determine
the resulting dictionary, what attributes are returned, and what is not.</p>
<p>Please note that in order to use this generator, you must install the python
<code class="docutils literal notranslate"><span class="pre">lxml</span></code> package.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>fobj</strong> (<em>File object</em><em> or </em><em>string path</em>) – Either a File-like object or a string path pointing to the file to
be parsed.</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>For example, if we wanted to load a Nessus report from disk and iterate
through the contents, it would simply be a matter of:</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="s1">&#39;example.nessus&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">nessus_file</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">report</span> <span class="o">=</span> <span class="n">NessusReportv2</span><span class="p">(</span><span class="n">nessus_file</span><span class="p">)</span>
<span class="gp">... </span>    <span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">report</span><span class="p">:</span>
<span class="gp">... </span>        <span class="nb">print</span><span class="p">(</span><span class="n">item</span><span class="p">)</span>
</pre></div>
</div>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.reports.nessusv2.NessusReportv2.next">
<span class="sig-name descname"><span class="pre">next</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/reports/nessusv2.md#NessusReportv2.next"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.reports.nessusv2.NessusReportv2.next" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the next ReportItem from the nessus file and return it as a
python dictionary.</p>
<p>Generally speaking this method is not called directly, but is instead
called as part of a loop.</p>
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
          <a href="tenable.sc.md" title="tenable.sc package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ot.graphql.md" title="tenable.ot.graphql package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.reports package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>