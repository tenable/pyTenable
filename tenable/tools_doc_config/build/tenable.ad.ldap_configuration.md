
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>tenable.ad.ldap_configuration package &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="_static/custom.css" />
    
    <script data-url_root="./" id="documentation_options" src="_static/documentation_options.js"></script>
    <script src="_static/jquery.js"></script>
    <script src="_static/underscore.js"></script>
    <script src="_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="genindex.md" />
    <link rel="search" title="Search" href="search.md" />
    <link rel="next" title="tenable.ad.lockout_policy package" href="tenable.ad.lockout_policy.md" />
    <link rel="prev" title="tenable.ad.infrastructure package" href="tenable.ad.infrastructure.md" /> 
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
          <a href="tenable.ad.lockout_policy.md" title="tenable.ad.lockout_policy package"
             accesskey="N">next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.infrastructure.md" title="tenable.ad.infrastructure package"
             accesskey="P">previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" accesskey="U">tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.ldap_configuration package</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <section id="module-tenable.ad.ldap_configuration">
<span id="tenable-ad-ldap-configuration-package"></span><h1>tenable.ad.ldap_configuration package<a class="headerlink" href="#module-tenable.ad.ldap_configuration" title="Permalink to this headline">¶</a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Permalink to this headline">¶</a></h2>
</section>
<section id="module-tenable.ad.ldap_configuration.api">
<span id="tenable-ad-ldap-configuration-api-module"></span><h2>tenable.ad.ldap_configuration.api module<a class="headerlink" href="#module-tenable.ad.ldap_configuration.api" title="Permalink to this headline">¶</a></h2>
<section id="ldap-configuration">
<h3>LDAP Configuration<a class="headerlink" href="#ldap-configuration" title="Permalink to this headline">¶</a></h3>
<p>Methods described in this section relate to the ldap configuration API.
These methods can be accessed at <code class="docutils literal notranslate"><span class="pre">TenableAD.ldap_configuration</span></code>.</p>
<dl class="py class hide-signature">
<dt class="sig sig-object py" id="tenable.ad.ldap_configuration.api.LDAPConfigurationAPI">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">LDAPConfigurationAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/api.md#LDAPConfigurationAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.ldap_configuration.api.LDAPConfigurationAPI" title="Permalink to this definition">¶</a></dt>
<dd><dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.ldap_configuration.api.LDAPConfigurationAPI.details">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/api.md#LDAPConfigurationAPI.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.ldap_configuration.api.LDAPConfigurationAPI.details" title="Permalink to this definition">¶</a></dt>
<dd><p>Get LDAP configuration singleton</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The LDAP configuration object</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">ldap_configuration</span><span class="o">.</span><span class="n">details</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.ldap_configuration.api.LDAPConfigurationAPI.update">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/api.md#LDAPConfigurationAPI.update"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.ldap_configuration.api.LDAPConfigurationAPI.update" title="Permalink to this definition">¶</a></dt>
<dd><p>Update LDAP configuration singleton</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>enabled</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a>) – Whether the ldap configuration enabled?</p></li>
<li><p><strong>url</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The URL of authentication provider server.</p></li>
<li><p><strong>search_user_dn</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DN of service account to use to authenticate the user.</p></li>
<li><p><strong>search_user_password</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The password of the service account used for authentication.</p></li>
<li><p><strong>user_search_base</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DN of the param object for items in LDAP server.</p></li>
<li><p><strong>user_search_filter</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – Used to change on what attribute the LDAP query is made to
authenticate the user.</p></li>
<li><p><strong>allowed_groups</strong> (<em>optional</em><em>, </em><em>List</em><em>[</em><em>Dict</em><em>]</em>) – The LDAP group a member need to be a member of so he can
authenticate. The below listed params are expected in
allowed groups dict.</p></li>
<li><p><strong>name</strong> (<em>required</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of group.</p></li>
<li><p><strong>default_role_ids</strong> (<em>required</em><em>, </em><em>List</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>]</em>) – The list default role identifiers.</p></li>
<li><p><strong>default_profile_id</strong> (<em>required</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The default profile identifier.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The LDAP configuration object</p>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">ldap_configuration</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">enabled</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">allowed_groups</span><span class="o">=</span><span class="p">[{</span>
<span class="gp">... </span>        <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="s1">&#39;group name&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;default_role_ids&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">],</span>
<span class="gp">... </span>        <span class="s1">&#39;default_profile_id&#39;</span><span class="p">:</span> <span class="mi">1</span>
<span class="gp">... </span>    <span class="p">}]</span>
<span class="gp">... </span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="id0">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">LDAPConfigurationAPI</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">api</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://restfly.readthedocs.io/en/latest/api/session.html#restfly.session.APISession" title="(in RESTfly v1.4.6)"><span class="pre">restfly.session.APISession</span></a></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/api.md#LDAPConfigurationAPI"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id0" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.base.md#id0" title="tenable.base.endpoint.APIEndpoint"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.base.endpoint.APIEndpoint</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="id1">
<span class="sig-name descname"><span class="pre">details</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/api.md#LDAPConfigurationAPI.details"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id1" title="Permalink to this definition">¶</a></dt>
<dd><p>Get LDAP configuration singleton</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The LDAP configuration object</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)">dict</a></p>
</dd>
</dl>
<p class="rubric">Examples</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">ldap_configuration</span><span class="o">.</span><span class="n">details</span><span class="p">()</span>
</pre></div>
</div>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="id2">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Dict" title="(in Python v3.10)"><span class="pre">Dict</span></a></span></span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/api.md#LDAPConfigurationAPI.update"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#id2" title="Permalink to this definition">¶</a></dt>
<dd><p>Update LDAP configuration singleton</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>enabled</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><em>bool</em></a>) – Whether the ldap configuration enabled?</p></li>
<li><p><strong>url</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The URL of authentication provider server.</p></li>
<li><p><strong>search_user_dn</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DN of service account to use to authenticate the user.</p></li>
<li><p><strong>search_user_password</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The password of the service account used for authentication.</p></li>
<li><p><strong>user_search_base</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The DN of the param object for items in LDAP server.</p></li>
<li><p><strong>user_search_filter</strong> (<em>optional</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – Used to change on what attribute the LDAP query is made to
authenticate the user.</p></li>
<li><p><strong>allowed_groups</strong> (<em>optional</em><em>, </em><em>List</em><em>[</em><em>Dict</em><em>]</em>) – The LDAP group a member need to be a member of so he can
authenticate. The below listed params are expected in
allowed groups dict.</p></li>
<li><p><strong>name</strong> (<em>required</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><em>str</em></a>) – The name of group.</p></li>
<li><p><strong>default_role_ids</strong> (<em>required</em><em>, </em><em>List</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a><em>]</em>) – The list default role identifiers.</p></li>
<li><p><strong>default_profile_id</strong> (<em>required</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><em>int</em></a>) – The default profile identifier.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>The LDAP configuration object</p>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">tad</span><span class="o">.</span><span class="n">ldap_configuration</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="gp">... </span>    <span class="n">enabled</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span>
<span class="gp">... </span>    <span class="n">allowed_groups</span><span class="o">=</span><span class="p">[{</span>
<span class="gp">... </span>        <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="s1">&#39;group name&#39;</span><span class="p">,</span>
<span class="gp">... </span>        <span class="s1">&#39;default_role_ids&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">],</span>
<span class="gp">... </span>        <span class="s1">&#39;default_profile_id&#39;</span><span class="p">:</span> <span class="mi">1</span>
<span class="gp">... </span>    <span class="p">}]</span>
<span class="gp">... </span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>

</dd></dl>

</section>
</section>
<section id="module-tenable.ad.ldap_configuration.schema">
<span id="tenable-ad-ldap-configuration-schema-module"></span><h2>tenable.ad.ldap_configuration.schema module<a class="headerlink" href="#module-tenable.ad.ldap_configuration.schema" title="Permalink to this headline">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.ldap_configuration.schema.LDAPConfigurationAllowedGroupsSchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">LDAPConfigurationAllowedGroupsSchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/schema.md#LDAPConfigurationAllowedGroupsSchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.ldap_configuration.schema.LDAPConfigurationAllowedGroupsSchema" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.ad.base.md#tenable.ad.base.schema.CamelCaseSchema" title="tenable.ad.base.schema.CamelCaseSchema"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.ad.base.schema.CamelCaseSchema</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.ldap_configuration.schema.LDAPConfigurationAllowedGroupsSchema.convert">
<span class="sig-name descname"><span class="pre">convert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/schema.md#LDAPConfigurationAllowedGroupsSchema.convert"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.ldap_configuration.schema.LDAPConfigurationAllowedGroupsSchema.convert" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="tenable.ad.ldap_configuration.schema.LDAPConfigurationSchema">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">LDAPConfigurationSchema</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">many</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">context</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">load_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dump_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.10)"><span class="pre">Union</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Sequence" title="(in Python v3.10)"><span class="pre">Sequence</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Set" title="(in Python v3.10)"><span class="pre">Set</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unknown</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.10)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/schema.md#LDAPConfigurationSchema"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.ldap_configuration.schema.LDAPConfigurationSchema" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <a class="reference internal" href="tenable.ad.base.md#tenable.ad.base.schema.CamelCaseSchema" title="tenable.ad.base.schema.CamelCaseSchema"><code class="xref py py-class docutils literal notranslate"><span class="pre">tenable.ad.base.schema.CamelCaseSchema</span></code></a></p>
<dl class="py method">
<dt class="sig sig-object py" id="tenable.ad.ldap_configuration.schema.LDAPConfigurationSchema.convert">
<span class="sig-name descname"><span class="pre">convert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="_modules/tenable/ad/ldap_configuration/schema.md#LDAPConfigurationSchema.convert"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#tenable.ad.ldap_configuration.schema.LDAPConfigurationSchema.convert" title="Permalink to this definition">¶</a></dt>
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
          <a href="tenable.ad.lockout_policy.md" title="tenable.ad.lockout_policy package"
             >next</a> |</li>
        <li class="right" >
          <a href="tenable.ad.infrastructure.md" title="tenable.ad.infrastructure package"
             >previous</a> |</li>
        <li class="nav-item nav-item-0"><a href="README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="tenable.ad.md" >tenable.ad package</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.ldap_configuration package</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>