
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.ldap_configuration.schema &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../../../_static/custom.css" />
    
    <script data-url_root="../../../../" id="documentation_options" src="../../../../_static/documentation_options.js"></script>
    <script src="../../../../_static/jquery.js"></script>
    <script src="../../../../_static/underscore.js"></script>
    <script src="../../../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../../../genindex.md" />
    <link rel="search" title="Search" href="../../../../search.md" /> 
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.ldap_configuration.schema</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.ldap_configuration.schema</h1><div class="highlight"><pre>
<span></span><span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">fields</span><span class="p">,</span> <span class="n">pre_load</span><span class="p">,</span> <span class="n">validate</span> <span class="k">as</span> <span class="n">v</span>
<span class="kn">from</span> <span class="nn">tenable.ad.base.schema</span> <span class="kn">import</span> <span class="n">CamelCaseSchema</span><span class="p">,</span> <span class="n">convert_keys_to_camel</span>


<div class="viewcode-block" id="LDAPConfigurationAllowedGroupsSchema"><a class="viewcode-back" href="../../../../tenable.ad.ldap_configuration.md#tenable.ad.ldap_configuration.schema.LDAPConfigurationAllowedGroupsSchema">[docs]</a><span class="k">class</span> <span class="nc">LDAPConfigurationAllowedGroupsSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">default_role_ids</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(),</span> <span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span>
                                   <span class="n">validate</span><span class="o">=</span><span class="n">v</span><span class="o">.</span><span class="n">Length</span><span class="p">(</span><span class="nb">min</span><span class="o">=</span><span class="mi">1</span><span class="p">))</span>
    <span class="n">default_profile_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<div class="viewcode-block" id="LDAPConfigurationAllowedGroupsSchema.convert"><a class="viewcode-back" href="../../../../tenable.ad.ldap_configuration.md#tenable.ad.ldap_configuration.schema.LDAPConfigurationAllowedGroupsSchema.convert">[docs]</a>    <span class="nd">@pre_load</span>
    <span class="k">def</span> <span class="nf">convert</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">return</span> <span class="n">convert_keys_to_camel</span><span class="p">(</span><span class="n">data</span><span class="p">)</span></div></div>


<div class="viewcode-block" id="LDAPConfigurationSchema"><a class="viewcode-back" href="../../../../tenable.ad.ldap_configuration.md#tenable.ad.ldap_configuration.schema.LDAPConfigurationSchema">[docs]</a><span class="k">class</span> <span class="nc">LDAPConfigurationSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">enabled</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Bool</span><span class="p">()</span>
    <span class="n">url</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">search_user_dn</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">search_user_password</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">user_search_base</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">user_search_filter</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">allowed_groups</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span>
        <span class="n">LDAPConfigurationAllowedGroupsSchema</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<div class="viewcode-block" id="LDAPConfigurationSchema.convert"><a class="viewcode-back" href="../../../../tenable.ad.ldap_configuration.md#tenable.ad.ldap_configuration.schema.LDAPConfigurationSchema.convert">[docs]</a>    <span class="nd">@pre_load</span>
    <span class="k">def</span> <span class="nf">convert</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">return</span> <span class="n">convert_keys_to_camel</span><span class="p">(</span><span class="n">data</span><span class="p">,</span> <span class="n">special</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;search_user_dn&#39;</span><span class="p">])</span></div></div>
</pre></div>

            <div class="clearer"></div>
          </div>
      </div>
      <div class="clearer"></div>
    </div>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.ldap_configuration.schema</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>