<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="next" title="tenable.ad.users package" href="tenable.ad.users.md" />
    <link rel="prev" title="tenable.ad.saml_configuration package" href="tenable.ad.saml_configuration.md" /> 
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
          <a href="tenable.ad.users.md" title="tenable.ad.users package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.saml_configuration.md" title="tenable.ad.saml_configuration package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" accesskey="U">tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.score package</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <section id="module-tenable.ad.score">
<span id="tenable-ad-score-package"></span><h1>tenable.ad.score package<a class="headerlink" href="#module-tenable.ad.score" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.ad.score.api">
<span id="tenable-ad-score-api-module"></span><h2>tenable.ad.score.api module<a class="headerlink" href="#module-tenable.ad.score.api" title="Permalink to this headline">¶</a></h2>
<section id="score">
<h3>Score<a class="headerlink" href="#score" title="Permalink to this headline">¶</a></h3>
<p>Methods described in this section relate to the the score API.
These methods can be accessed at <code class="docutils literal notranslate"><span class="pre">TenableAD.score</span></code>.</p>
<dl class="py class hide-signature">
<dt class="sig sig-object py" id="tenable.ad.score.api.ScoreAPI">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">ScoreAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/score/api.md#ScoreAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.score.api.ScoreAPI" title="Permalink to this definition">¶</a></dt>
<dd><dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.score.api.ScoreAPI.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">profile_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/score/api.md#ScoreAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.score.api.ScoreAPI.list" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the list of directories score by profile.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>Option-1</strong> – <dl class="simple">
<dt>profile_id (str):</dt><dd><p>The profile instance identifier.</p>
</dd>
<dt>directory_ids (optional, List(int)):</dt><dd><p>The list of directory_ids.</p>
</dd>
<dt>checker_ids (optional, List(int)):</dt><dd><p>The list of checker_ids.</p>
</dd>
<dt>reason_ids (optional, List(int)):</dt><dd><p>The list of reason_ids.</p>
</dd>
</dl>
</p></li>
<li><p><strong>Option-2</strong> – <dl class="simple">
<dt>profile_id (str):</dt><dd><p>The profile instance identifier.</p>
</dd>
<dt>directory_ids (optional, str):</dt><dd><p>The directory_id instance identifier.</p>
</dd>
<dt>checker_ids (optional, str):</dt><dd><p>The checker_id instance identifier.</p>
</dd>
<dt>reason_ids (optional, str):</dt><dd><p>The reason_id instance identifier.</p>
</dd>
</dl>
</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>List of scores of different directories in the instance.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>With single directory_ids, checker_ids, reason_ids</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">score</span><span class="o">.</span><span class="n">list</span><span class="p">(</span><span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_ids</span><span class="o">=</span><span class="s1">&#39;3&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">checker_ids</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">reason_ids</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>With multiple directory_ids, checker_ids, reason_ids</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">score</span><span class="o">.</span><span class="n">list</span><span class="p">(</span><span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">],</span>
<span class="gp">... </span>    <span class="n">checker_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">],</span>
<span class="gp">... </span>    <span class="n">reason_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">])</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">ScoreAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/score/api.md#ScoreAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id0" title="tenable.base.endpoint.APIEndpoint"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.endpoint.APIEndpoint</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">profile_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/score/api.md#ScoreAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the list of directories score by profile.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>Option-1</strong> – <dl class="simple">
<dt>profile_id (str):</dt><dd><p>The profile instance identifier.</p>
</dd>
<dt>directory_ids (optional, List(int)):</dt><dd><p>The list of directory_ids.</p>
</dd>
<dt>checker_ids (optional, List(int)):</dt><dd><p>The list of checker_ids.</p>
</dd>
<dt>reason_ids (optional, List(int)):</dt><dd><p>The list of reason_ids.</p>
</dd>
</dl>
</p></li>
<li><p><strong>Option-2</strong> – <dl class="simple">
<dt>profile_id (str):</dt><dd><p>The profile instance identifier.</p>
</dd>
<dt>directory_ids (optional, str):</dt><dd><p>The directory_id instance identifier.</p>
</dd>
<dt>checker_ids (optional, str):</dt><dd><p>The checker_id instance identifier.</p>
</dd>
<dt>reason_ids (optional, str):</dt><dd><p>The reason_id instance identifier.</p>
</dd>
</dl>
</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>List of scores of different directories in the instance.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<p>With single directory_ids, checker_ids, reason_ids</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">score</span><span class="o">.</span><span class="n">list</span><span class="p">(</span><span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_ids</span><span class="o">=</span><span class="s1">&#39;3&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">checker_ids</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">reason_ids</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p>With multiple directory_ids, checker_ids, reason_ids</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">score</span><span class="o">.</span><span class="n">list</span><span class="p">(</span><span class="n">profile_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">directory_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">],</span>
<span class="gp">... </span>    <span class="n">checker_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">],</span>
<span class="gp">... </span>    <span class="n">reason_ids</span><span class="o">=</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">])</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
</section>
</section>
<section id="module-tenable.ad.score.schema">
<span id="tenable-ad-score-schema-module"></span><h2>tenable.ad.score.schema module<a class="headerlink" href="#module-tenable.ad.score.schema" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.score.schema.ScoreRules">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">ScoreRules</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="pre">*,</span> <span class="pre">load_default:</span> <span class="pre">typing.Any</span> <span class="pre">=</span> <span class="pre">&lt;marshmallow.missing&gt;,</span> <span class="pre">missing:</span> <span class="pre">typing.Any</span> <span class="pre">=</span> <span class="pre">&lt;marshmallow.missing&gt;,</span> <span class="pre">dump_default:</span> <span class="pre">typing.Any</span> <span class="pre">=</span> <span class="pre">&lt;marshmallow.missing&gt;,</span> <span class="pre">default:</span> <span class="pre">typing.Any</span> <span class="pre">=</span> <span class="pre">&lt;marshmallow.missing&gt;,</span> <span class="pre">data_key:</span> <span class="pre">typing.Optional[str]</span> <span class="pre">=</span> <span class="pre">None,</span> <span class="pre">attribute:</span> <span class="pre">typing.Optional[str]</span> <span class="pre">=</span> <span class="pre">None,</span> <span class="pre">validate:</span> <span class="pre">typing.Union[None,</span> <span class="pre">typing.Callable[[typing.Any],</span> <span class="pre">typing.Any],</span> <span class="pre">typing.Iterable[typing.Callable[[typing.Any],</span> <span class="pre">typing.Any]]]</span> <span class="pre">=</span> <span class="pre">None,</span> <span class="pre">required:</span> <span class="pre">bool</span> <span class="pre">=</span> <span class="pre">False,</span> <span class="pre">allow_none:</span> <span class="pre">typing.Optional[bool]</span> <span class="pre">=</span> <span class="pre">None,</span> <span class="pre">load_only:</span> <span class="pre">bool</span> <span class="pre">=</span> <span class="pre">False,</span> <span class="pre">dump_only:</span> <span class="pre">bool</span> <span class="pre">=</span> <span class="pre">False,</span> <span class="pre">error_messages:</span> <span class="pre">typing.Optional[dict[str,</span> <span class="pre">str]]</span> <span class="pre">=</span> <span class="pre">None,</span> <span class="pre">metadata:</span> <span class="pre">typing.Optional[typing.Mapping[str,</span> <span class="pre">typing.Any]]</span> <span class="pre">=</span> <span class="pre">None,</span> <span class="pre">**additional_metadata</span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/score/schema.md#ScoreRules"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.score.schema.ScoreRules" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">marshmallow.fields.Field</span></code></p>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.score.schema.ScoreSchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">ScoreSchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/score/schema.md#ScoreSchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.score.schema.ScoreSchema" title="Permalink to this definition">¶</a></dt>
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
          <a href="tenable.ad.users.md" title="tenable.ad.users package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.saml_configuration.md" title="tenable.ad.saml_configuration package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" >tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.score package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>