<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="next" title="tenable.ad.saml_configuration package" href="tenable.ad.saml_configuration.md" />
    <link rel="prev" title="tenable.ad.profiles package" href="tenable.ad.profiles.md" /> 
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
          <a href="tenable.ad.saml_configuration.md" title="tenable.ad.saml_configuration package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.profiles.md" title="tenable.ad.profiles package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" accesskey="U">tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.roles package</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <section id="module-tenable.ad.roles">
<span id="tenable-ad-roles-package"></span><h1>tenable.ad.roles package<a class="headerlink" href="#module-tenable.ad.roles" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.ad.roles.api">
<span id="tenable-ad-roles-api-module"></span><h2>tenable.ad.roles.api module<a class="headerlink" href="#module-tenable.ad.roles.api" title="Permalink to this headline">¶</a></h2>
<section id="roles">
<h3>Roles<a class="headerlink" href="#roles" title="Permalink to this headline">¶</a></h3>
<p>Methods described in this section relate to the roles API.
These methods can be accessed at <code class="docutils literal notranslate"><span class="pre">TenableAD.roles</span></code>.</p>
<dl class="py class hide-signature">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">RolesAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI" title="Permalink to this definition">¶</a></dt>
<dd><dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.copy_role">
<span class="sig-name descname"><span class="pre">copy_role</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">from_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.copy_role"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.copy_role" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates a new role from another role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>from_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier user wants to copy.</p></li>
<li><p><strong>name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of new role.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the copied role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">copy_role</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">from_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;Copied name&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.create">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">description</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.create"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.create" title="Permalink to this definition">¶</a></dt>
<dd><p>Create a new role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of role.</p></li>
<li><p><strong>description</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The description of role.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The created role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a>[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a>]</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;Admin&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">description</span><span class="o">=</span><span class="s2">&quot;all privileges&quot;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.default_roles">
<span class="sig-name descname"><span class="pre">default_roles</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.default_roles"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.default_roles" title="Permalink to this definition">¶</a></dt>
<dd><p>Return the default roles for user creation</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The default roles object.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a>[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a>]</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">default_roles</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.delete">
<span class="sig-name descname"><span class="pre">delete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.delete"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.delete" title="Permalink to this definition">¶</a></dt>
<dd><p>Delete an existing role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.details">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.details" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the details of a specific role.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">details</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.list" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieve all roles</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The list of roles objects</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a>[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a>]</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">list</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.replace_role_permissions">
<span class="sig-name descname"><span class="pre">replace_role_permissions</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">permissions</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.replace_role_permissions"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.replace_role_permissions" title="Permalink to this definition">¶</a></dt>
<dd><p>Replace permission list for a role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p></li>
<li><p><strong>permissions</strong> (<em>List</em><em>[</em><em>Dict</em><em>]</em>) – The list of permissions dictionaries.
Below are the values expected in dictionaries</p></li>
<li><p><strong>entity_name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of entity.</p></li>
<li><p><strong>action</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The code of action to perform.</p></li>
<li><p><strong>entity_ids</strong> (<em>List</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>]</em>) – The list of entity identifiers.</p></li>
<li><p><strong>dynamic_id</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The dynamicId to use associated with the action.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the update permissions role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">replace_role_permissions</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">permissions</span><span class="o">=</span><span class="p">[{</span>
<span class="gp">... </span>        <span class="s1">&#39;entity_name&#39;</span><span class="p">:</span><span class="s1">&#39;dashboard&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;action&#39;</span><span class="p">:</span><span class="s1">&#39;action&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;entity_ids&#39;</span><span class="p">:[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">],</span>
<span class="gp">... </span>        <span class="s1">&#39;dynamic_id&#39;</span><span class="p">:</span> <span class="kc">None</span>
<span class="gp">... </span>    <span class="p">}]</span>
<span class="gp">... </span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.api.RolesAPI.update">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.update"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.api.RolesAPI.update" title="Permalink to this definition">¶</a></dt>
<dd><p>Update an existing role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p></li>
<li><p><strong>name</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of role.</p></li>
<li><p><strong>description</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The description of role.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The updated widget object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;Basic&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">RolesAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id0" title="tenable.base.endpoint.APIEndpoint"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.endpoint.APIEndpoint</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">copy_role</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">from_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.copy_role"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates a new role from another role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>from_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier user wants to copy.</p></li>
<li><p><strong>name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of new role.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the copied role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">copy_role</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">from_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;Copied name&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id2">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">description</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.create"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id2" title="Permalink to this definition">¶</a></dt>
<dd><p>Create a new role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of role.</p></li>
<li><p><strong>description</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The description of role.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The created role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a>[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a>]</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;Admin&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">description</span><span class="o">=</span><span class="s2">&quot;all privileges&quot;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id3">
<span class="sig-name descname"><span class="pre">default_roles</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.default_roles"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id3" title="Permalink to this definition">¶</a></dt>
<dd><p>Return the default roles for user creation</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The default roles object.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a>[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a>]</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">default_roles</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id4">
<span class="sig-name descname"><span class="pre">delete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.delete"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id4" title="Permalink to this definition">¶</a></dt>
<dd><p>Delete an existing role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id5">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id5" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieves the details of a specific role.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">details</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id6">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.list"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id6" title="Permalink to this definition">¶</a></dt>
<dd><p>Retrieve all roles</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The list of roles objects</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#list" title="(in Python v3.10)">list</a>[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a>]</p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">list</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id7">
<span class="sig-name descname"><span class="pre">replace_role_permissions</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">permissions</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.10)"><span class="pre">List</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.replace_role_permissions"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id7" title="Permalink to this definition">¶</a></dt>
<dd><p>Replace permission list for a role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p></li>
<li><p><strong>permissions</strong> (<em>List</em><em>[</em><em>Dict</em><em>]</em>) – The list of permissions dictionaries.
Below are the values expected in dictionaries</p></li>
<li><p><strong>entity_name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of entity.</p></li>
<li><p><strong>action</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The code of action to perform.</p></li>
<li><p><strong>entity_ids</strong> (<em>List</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>]</em>) – The list of entity identifiers.</p></li>
<li><p><strong>dynamic_id</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The dynamicId to use associated with the action.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>the update permissions role object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">replace_role_permissions</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">permissions</span><span class="o">=</span><span class="p">[{</span>
<span class="gp">... </span>        <span class="s1">&#39;entity_name&#39;</span><span class="p">:</span><span class="s1">&#39;dashboard&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;action&#39;</span><span class="p">:</span><span class="s1">&#39;action&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;entity_ids&#39;</span><span class="p">:[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">],</span>
<span class="gp">... </span>        <span class="s1">&#39;dynamic_id&#39;</span><span class="p">:</span> <span class="kc">None</span>
<span class="gp">... </span>    <span class="p">}]</span>
<span class="gp">... </span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="id8">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">role_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/roles/api.md#RolesAPI.update"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id8" title="Permalink to this definition">¶</a></dt>
<dd><p>Update an existing role</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>role_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The role instance identifier.</p></li>
<li><p><strong>name</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of role.</p></li>
<li><p><strong>description</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The description of role.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The updated widget object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">roles</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">role_id</span><span class="o">=</span><span class="s1">&#39;1&#39;</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">name</span><span class="o">=</span><span class="s1">&#39;Basic&#39;</span>
<span class="gp">... </span>    <span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</dd></dl>
</section>
</section>
<section id="module-tenable.ad.roles.schema">
<span id="tenable-ad-roles-schema-module"></span><h2>tenable.ad.roles.schema module<a class="headerlink" href="#module-tenable.ad.roles.schema" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.roles.schema.RolePermissionsSchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">RolePermissionsSchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/roles/schema.md#RolePermissionsSchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.schema.RolePermissionsSchema" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.ad.base.md#tenable.ad.base.schema.CamelCaseSchema" title="tenable.ad.base.schema.CamelCaseSchema"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.ad.base.schema.CamelCaseSchema</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.roles.schema.RolePermissionsSchema.keys_to_camel">
<span class="sig-name descname"><span class="pre">keys_to_camel</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/roles/schema.md#RolePermissionsSchema.keys_to_camel"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.schema.RolePermissionsSchema.keys_to_camel" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.roles.schema.RoleSchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">RoleSchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/roles/schema.md#RoleSchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.roles.schema.RoleSchema" title="Permalink to this definition">¶</a></dt>
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
          <a href="tenable.ad.saml_configuration.md" title="tenable.ad.saml_configuration package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.profiles.md" title="tenable.ad.profiles package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" >tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.roles package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>