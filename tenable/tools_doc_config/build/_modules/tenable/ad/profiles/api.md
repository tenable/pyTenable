
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.profiles.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.profiles.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.profiles.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Profiles</span>
<span class="sd">=============</span>

<span class="sd">Methods described in this section relate to the profiles API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.profiles``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ProfilesAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">.schema</span> <span class="kn">import</span> <span class="n">ProfileSchema</span>


<div class="viewcode-block" id="ProfilesAPI"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI">[docs]</a><span class="k">class</span> <span class="nc">ProfilesAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;profiles&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">ProfileSchema</span><span class="p">()</span>

<div class="viewcode-block" id="ProfilesAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieve all profiles</span>

<span class="sd">        Returns:</span>
<span class="sd">            list[dict]:</span>
<span class="sd">                The list of profile objects</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="ProfilesAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">directories</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="nb">int</span><span class="p">]</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Create a profile</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of new profile.</span>
<span class="sd">            directories (List[int]):</span>
<span class="sd">                The list of directory identifiers.</span>

<span class="sd">        Return:</span>
<span class="sd">            list[dict]:</span>
<span class="sd">                The created profile objects</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.create(</span>
<span class="sd">            ...     name=&#39;ExampleProfile&#39;,</span>
<span class="sd">            ...     directories=[1, 2]</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">[</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
                <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
                <span class="s1">&#39;directories&#39;</span><span class="p">:</span> <span class="n">directories</span>
            <span class="p">}))</span>
        <span class="p">]</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="ProfilesAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span>
                <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for a specific profile</span>

<span class="sd">        Args:</span>
<span class="sd">            profile_id (str):</span>
<span class="sd">                The profile instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The profile object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.details(&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">))</span></div>

<div class="viewcode-block" id="ProfilesAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Update an existing profile</span>

<span class="sd">        Args:</span>
<span class="sd">            profile_id (str):</span>
<span class="sd">                The profile instance identifier.</span>
<span class="sd">            name (optional, str):</span>
<span class="sd">                The name of profile.</span>
<span class="sd">            deleted (optional, bool):</span>
<span class="sd">                is the profile deleted?</span>
<span class="sd">            directories (optional, List[int]):</span>
<span class="sd">                The list of directory ids.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The updated profile object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.update(</span>
<span class="sd">            ...     profile_id=&#39;1&#39;,</span>
<span class="sd">            ...     name=&#39;EDITED&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>

<div class="viewcode-block" id="ProfilesAPI.delete"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Delete an existing profile</span>

<span class="sd">        Args:</span>
<span class="sd">            profile_id (str):</span>
<span class="sd">                The profile instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.delete(profile_id=&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_delete</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span></div>

<div class="viewcode-block" id="ProfilesAPI.copy_profile"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.copy_profile">[docs]</a>    <span class="k">def</span> <span class="nf">copy_profile</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                     <span class="n">from_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                     <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                     <span class="n">directories</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="nb">int</span><span class="p">]</span>
                     <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new profile from another profile</span>

<span class="sd">        Args:</span>
<span class="sd">            from_id (str):</span>
<span class="sd">                The profile instance identifier user wants to copy.</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of new profile.</span>
<span class="sd">            directories (List[int]):</span>
<span class="sd">                The list of directory ids.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The copied role object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.copy_profile(</span>
<span class="sd">            ...     from_id=&#39;1&#39;,</span>
<span class="sd">            ...     name=&#39;Copied name&#39;,</span>
<span class="sd">            ...     directories=[1, 2]</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
            <span class="s1">&#39;directories&#39;</span><span class="p">:</span> <span class="n">directories</span>
        <span class="p">}))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;from/</span><span class="si">{</span><span class="n">from_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>

<div class="viewcode-block" id="ProfilesAPI.commit"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.commit">[docs]</a>    <span class="k">def</span> <span class="nf">commit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Commits change of the related profile</span>

<span class="sd">        Args:</span>
<span class="sd">            profile_id (str):</span>
<span class="sd">                The profile instance identifier.</span>

<span class="sd">        Return:</span>
<span class="sd">            None</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.commit(&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s1">/commit&#39;</span><span class="p">)</span></div>

<div class="viewcode-block" id="ProfilesAPI.unstage"><a class="viewcode-back" href="../../../../tenable.ad.profiles.md#tenable.ad.profiles.api.ProfilesAPI.unstage">[docs]</a>    <span class="k">def</span> <span class="nf">unstage</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span>
                <span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Unstages changes of the related profile</span>

<span class="sd">        Args:</span>
<span class="sd">            profile_id (str):</span>
<span class="sd">                The profile instance identifier.</span>

<span class="sd">        Return:</span>
<span class="sd">            None</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.profiles.unstage(&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s1">/unstage&#39;</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.profiles.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>