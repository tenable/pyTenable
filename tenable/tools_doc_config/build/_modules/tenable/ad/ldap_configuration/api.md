
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.ldap_configuration.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.ldap_configuration.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.ldap_configuration.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">LDAP Configuration</span>
<span class="sd">=============</span>

<span class="sd">Methods described in this section relate to the ldap configuration API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.ldap_configuration``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: LDAPConfigurationAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.ad.ldap_configuration.schema</span> <span class="kn">import</span> <span class="n">LDAPConfigurationSchema</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>


<div class="viewcode-block" id="LDAPConfigurationAPI"><a class="viewcode-back" href="../../../../tenable.ad.ldap_configuration.md#tenable.ad.ldap_configuration.api.LDAPConfigurationAPI">[docs]</a><span class="k">class</span> <span class="nc">LDAPConfigurationAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;ldap-configuration&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">LDAPConfigurationSchema</span><span class="p">()</span>

<div class="viewcode-block" id="LDAPConfigurationAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.ldap_configuration.md#tenable.ad.ldap_configuration.api.LDAPConfigurationAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Get LDAP configuration singleton</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The LDAP configuration object</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.ldap_configuration.details()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">())</span></div>

<div class="viewcode-block" id="LDAPConfigurationAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.ldap_configuration.md#tenable.ad.ldap_configuration.api.LDAPConfigurationAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Update LDAP configuration singleton</span>

<span class="sd">        Args:</span>
<span class="sd">            enabled (optional, bool):</span>
<span class="sd">                Whether the ldap configuration enabled?</span>
<span class="sd">            url (optional, str):</span>
<span class="sd">                The URL of authentication provider server.</span>
<span class="sd">            search_user_dn (optional, str):</span>
<span class="sd">                The DN of service account to use to authenticate the user.</span>
<span class="sd">            search_user_password (optional, str):</span>
<span class="sd">                The password of the service account used for authentication.</span>
<span class="sd">            user_search_base (optional, str):</span>
<span class="sd">                The DN of the param object for items in LDAP server.</span>
<span class="sd">            user_search_filter (optional, str):</span>
<span class="sd">                Used to change on what attribute the LDAP query is made to</span>
<span class="sd">                authenticate the user.</span>
<span class="sd">            allowed_groups (optional, List[Dict]):</span>
<span class="sd">                The LDAP group a member need to be a member of so he can</span>
<span class="sd">                authenticate. The below listed params are expected in</span>
<span class="sd">                allowed groups dict.</span>
<span class="sd">            name (required, str):</span>
<span class="sd">                The name of group.</span>
<span class="sd">            default_role_ids (required, List[int]):</span>
<span class="sd">                The list default role identifiers.</span>
<span class="sd">            default_profile_id (required, int):</span>
<span class="sd">                The default profile identifier.</span>

<span class="sd">        Return:</span>
<span class="sd">            The LDAP configuration object</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.ldap_configuration.update(</span>
<span class="sd">            ...     enabled=True,</span>
<span class="sd">            ...     allowed_groups=[{</span>
<span class="sd">            ...         &#39;name&#39;: &#39;group name&#39;,</span>
<span class="sd">            ...         &#39;default_role_ids&#39;: [1, 2],</span>
<span class="sd">            ...         &#39;default_profile_id&#39;: 1</span>
<span class="sd">            ...     }]</span>
<span class="sd">            ... )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.ldap_configuration.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>