<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../../genindex.md" />
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.session</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.ad.session</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Tenable.ad session</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">import</span> <span class="nn">warnings</span>
<span class="kn">import</span> <span class="nn">os</span>
<span class="kn">from</span> <span class="nn">tenable.base.platform</span> <span class="kn">import</span> <span class="n">APIPlatform</span>
<span class="kn">from</span> <span class="nn">.about</span> <span class="kn">import</span> <span class="n">AboutAPI</span>
<span class="kn">from</span> <span class="nn">.api_keys</span> <span class="kn">import</span> <span class="n">APIKeyAPI</span>
<span class="kn">from</span> <span class="nn">.attack_types.api</span> <span class="kn">import</span> <span class="n">AttackTypesAPI</span>
<span class="kn">from</span> <span class="nn">.category.api</span> <span class="kn">import</span> <span class="n">CategoryAPI</span>
<span class="kn">from</span> <span class="nn">.checker.api</span> <span class="kn">import</span> <span class="n">CheckerAPI</span>
<span class="kn">from</span> <span class="nn">.checker_option.api</span> <span class="kn">import</span> <span class="n">CheckerOptionAPI</span>
<span class="kn">from</span> <span class="nn">.dashboard.api</span> <span class="kn">import</span> <span class="n">DashboardAPI</span>
<span class="kn">from</span> <span class="nn">.directories.api</span> <span class="kn">import</span> <span class="n">DirectoriesAPI</span>
<span class="kn">from</span> <span class="nn">.infrastructure.api</span> <span class="kn">import</span> <span class="n">InfrastructureAPI</span>
<span class="kn">from</span> <span class="nn">.ldap_configuration.api</span> <span class="kn">import</span> <span class="n">LDAPConfigurationAPI</span>
<span class="kn">from</span> <span class="nn">.lockout_policy.api</span> <span class="kn">import</span> <span class="n">LockoutPolicyAPI</span>
<span class="kn">from</span> <span class="nn">.preference.api</span> <span class="kn">import</span> <span class="n">PreferenceAPI</span>
<span class="kn">from</span> <span class="nn">.profiles.api</span> <span class="kn">import</span> <span class="n">ProfilesAPI</span>
<span class="kn">from</span> <span class="nn">.roles.api</span> <span class="kn">import</span> <span class="n">RolesAPI</span>
<span class="kn">from</span> <span class="nn">.saml_configuration.api</span> <span class="kn">import</span> <span class="n">SAMLConfigurationAPI</span>
<span class="kn">from</span> <span class="nn">.score.api</span> <span class="kn">import</span> <span class="n">ScoreAPI</span>
<span class="kn">from</span> <span class="nn">.users.api</span> <span class="kn">import</span> <span class="n">UsersAPI</span>
<span class="kn">from</span> <span class="nn">.widget.api</span> <span class="kn">import</span> <span class="n">WidgetsAPI</span>
<div class="viewcode-block" id="TenableAD"><a class="viewcode-back" href="../../../tenable.ad.md#tenable.ad.TenableAD">[docs]</a><span class="k">class</span> <span class="nc">TenableAD</span><span class="p">(</span><span class="n">APIPlatform</span><span class="p">):</span>
    <span class="n">_env_base</span> <span class="o">=</span> <span class="s1">&#39;TAD&#39;</span>
    <span class="n">_base_path</span> <span class="o">=</span> <span class="s1">&#39;api&#39;</span>
    <span class="n">_conv_json</span> <span class="o">=</span> <span class="kc">True</span>
    <span class="k">def</span> <span class="nf">_session_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="n">msg</span> <span class="o">=</span> <span class="s1">&#39;Session Auth isn</span><span class="se">\&#39;</span><span class="s1">t supported with the Tenable.ad APIs&#39;</span>
        <span class="n">warnings</span><span class="o">.</span><span class="n">warn</span><span class="p">(</span><span class="n">msg</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_log</span><span class="o">.</span><span class="n">warning</span><span class="p">(</span><span class="n">msg</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">_key_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">api_key</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_session</span><span class="o">.</span><span class="n">headers</span><span class="o">.</span><span class="n">update</span><span class="p">({</span>
            <span class="s1">&#39;X-API-Key&#39;</span><span class="p">:</span> <span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">api_key</span><span class="si">}</span><span class="s1">&#39;</span>
        <span class="p">})</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">=</span> <span class="s1">&#39;keys&#39;</span>
    <span class="k">def</span> <span class="nf">_authenticate</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;_key_auth_dict&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;_key_auth_dict&#39;</span><span class="p">,</span> <span class="p">{</span>
            <span class="s1">&#39;api_key&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;api_key&#39;</span><span class="p">,</span>
                                  <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="si">}</span><span class="s1">_API_KEY&#39;</span><span class="p">)</span>
                                  <span class="p">)</span>
        <span class="p">})</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">_authenticate</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">about</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad About APIs &lt;about&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AboutAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">api_keys</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad API-Keys APIs &lt;api_keys&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">APIKeyAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">attack_types</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Attack Types APIs &lt;attack_types&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AttackTypesAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">category</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Category APIs &lt;category&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">CategoryAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">checker</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Checker APIs &lt;checker&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">CheckerAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">checker_option</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Checker option APIs &lt;checker_option&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">CheckerOptionAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">dashboard</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Dashboard APIs &lt;dashboard&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">DashboardAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">directories</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Directories APIs &lt;directories&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">DirectoriesAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">infrastructure</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Infrastructure APIs &lt;infrastructure&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">InfrastructureAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">ldap_configuration</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad LDAP Configuration APIs &lt;ldap_configuration&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">LDAPConfigurationAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">lockout_policy</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Lockout Policy APIs &lt;lockout_policy&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">LockoutPolicyAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">preference</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Preference APIs &lt;preference&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">PreferenceAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">profiles</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Profiles APIs &lt;profiles&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">ProfilesAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">roles</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Roles APIs &lt;roles&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">RolesAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">saml_configuration</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad SAML configuration APIs &lt;saml_configuration&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">SAMLConfigurationAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">score</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Score APIs &lt;score&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">ScoreAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">users</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Users APIs &lt;users&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">UsersAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">widgets</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ad Widget APIs &lt;widget&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">WidgetsAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span></div>
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
          <a href="../../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.session</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>