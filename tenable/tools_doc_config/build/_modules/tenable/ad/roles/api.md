
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.roles.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.roles.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.roles.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Roles</span>
<span class="sd">=============</span>

<span class="sd">Methods described in this section relate to the roles API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.roles``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: RolesAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">ValidationError</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">.schema</span> <span class="kn">import</span> <span class="n">RoleSchema</span><span class="p">,</span> <span class="n">RolePermissionsSchema</span>


<div class="viewcode-block" id="RolesAPI"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI">[docs]</a><span class="k">class</span> <span class="nc">RolesAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;roles&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">RoleSchema</span><span class="p">()</span>

<div class="viewcode-block" id="RolesAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieve all roles</span>

<span class="sd">        Returns:</span>
<span class="sd">            list[dict]:</span>
<span class="sd">                The list of roles objects</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="RolesAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">description</span><span class="p">:</span> <span class="nb">int</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Create a new role</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of role.</span>
<span class="sd">            description (str):</span>
<span class="sd">               The description of role.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list[dict]:</span>
<span class="sd">                The created role object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.create(</span>
<span class="sd">            ...     name=&#39;Admin&#39;,</span>
<span class="sd">            ...     description=&quot;all privileges&quot;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">[</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
                <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
                <span class="s1">&#39;description&#39;</span><span class="p">:</span> <span class="n">description</span>
            <span class="p">}))</span>
        <span class="p">]</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="RolesAPI.default_roles"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.default_roles">[docs]</a>    <span class="k">def</span> <span class="nf">default_roles</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Return the default roles for user creation</span>

<span class="sd">        Returns:</span>
<span class="sd">            list[dict]:</span>
<span class="sd">                The default roles object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.default_roles()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="s1">&#39;user-creation-defaults&#39;</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="RolesAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">role_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details of a specific role.</span>

<span class="sd">        Args:</span>
<span class="sd">            role_id (str):</span>
<span class="sd">                The role instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                the role object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.details(</span>
<span class="sd">            ...     role_id=&#39;1&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">role_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">))</span></div>

<div class="viewcode-block" id="RolesAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">role_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Update an existing role</span>

<span class="sd">        Args:</span>
<span class="sd">            role_id (str):</span>
<span class="sd">                The role instance identifier.</span>
<span class="sd">            name (optional, str):</span>
<span class="sd">                The name of role.</span>
<span class="sd">            description (optional, str):</span>
<span class="sd">               The description of role.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The updated widget object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.update(</span>
<span class="sd">            ...     role_id=&#39;1&#39;,</span>
<span class="sd">            ...     name=&#39;Basic&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">role_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>

<div class="viewcode-block" id="RolesAPI.delete"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">role_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Delete an existing role</span>

<span class="sd">        Args:</span>
<span class="sd">            role_id (str):</span>
<span class="sd">                The role instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.delete(</span>
<span class="sd">            ...     role_id=&#39;1&#39;,</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_delete</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">role_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span></div>

<div class="viewcode-block" id="RolesAPI.copy_role"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.copy_role">[docs]</a>    <span class="k">def</span> <span class="nf">copy_role</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                  <span class="n">from_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                  <span class="n">name</span><span class="p">:</span> <span class="nb">str</span>
                  <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new role from another role</span>

<span class="sd">        Args:</span>
<span class="sd">            from_id (str):</span>
<span class="sd">                The role instance identifier user wants to copy.</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of new role.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                the copied role object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.copy_role(</span>
<span class="sd">            ...     from_id=&#39;1&#39;,</span>
<span class="sd">            ...     name=&#39;Copied name&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span>
        <span class="p">}))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;from/</span><span class="si">{</span><span class="n">from_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>

<div class="viewcode-block" id="RolesAPI.replace_role_permissions"><a class="viewcode-back" href="../../../../tenable.ad.roles.md#tenable.ad.roles.api.RolesAPI.replace_role_permissions">[docs]</a>    <span class="k">def</span> <span class="nf">replace_role_permissions</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                                 <span class="n">role_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                                 <span class="n">permissions</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]</span>
                                 <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Replace permission list for a role</span>

<span class="sd">        Args:</span>
<span class="sd">            role_id (str):</span>
<span class="sd">                The role instance identifier.</span>
<span class="sd">            permissions (List[Dict]) :</span>
<span class="sd">                The list of permissions dictionaries.</span>
<span class="sd">                Below are the values expected in dictionaries</span>
<span class="sd">            entity_name (str):</span>
<span class="sd">                The name of entity.</span>
<span class="sd">            action (str):</span>
<span class="sd">                The code of action to perform.</span>
<span class="sd">            entity_ids (List[int]):</span>
<span class="sd">                The list of entity identifiers.</span>
<span class="sd">            dynamic_id (optional, str):</span>
<span class="sd">                The dynamicId to use associated with the action.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                the update permissions role object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.roles.replace_role_permissions(</span>
<span class="sd">            ...     role_id=&#39;1&#39;,</span>
<span class="sd">            ...     permissions=[{</span>
<span class="sd">            ...         &#39;entity_name&#39;:&#39;dashboard&#39;,</span>
<span class="sd">            ...         &#39;action&#39;:&#39;action&#39;,</span>
<span class="sd">            ...         &#39;entity_ids&#39;:[1, 2],</span>
<span class="sd">            ...         &#39;dynamic_id&#39;: None</span>
<span class="sd">            ...     }]</span>
<span class="sd">            ... )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">RolePermissionsSchema</span><span class="p">()</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="n">schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">permissions</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_put</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">role_id</span><span class="si">}</span><span class="s1">/permissions&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.roles.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>