
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.users.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.users.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.users.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Users</span>
<span class="sd">=============</span>

<span class="sd">Methods described in this section relate to the users API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.users``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: UsersAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">INCLUDE</span>
<span class="kn">from</span> <span class="nn">restfly.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">.schema</span> <span class="kn">import</span> <span class="n">UserSchema</span><span class="p">,</span> <span class="n">UserInfoSchema</span>


<div class="viewcode-block" id="UsersAPI"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI">[docs]</a><span class="k">class</span> <span class="nc">UsersAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;users&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">UserSchema</span><span class="p">()</span>

<div class="viewcode-block" id="UsersAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieve all users</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                The list of users objects</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">email</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">password</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Create users</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of new user.</span>
<span class="sd">            email (str):</span>
<span class="sd">                The email address of the user.</span>
<span class="sd">            password (str):</span>
<span class="sd">                The password for the new user.</span>
<span class="sd">            surname (optional, str):</span>
<span class="sd">                The surname of new user.</span>
<span class="sd">            department (optional, str):</span>
<span class="sd">                The department of user.</span>
<span class="sd">            biography (optional, str):</span>
<span class="sd">                The biography of user.</span>
<span class="sd">            active (optional, bool):</span>
<span class="sd">                is the user active?</span>
<span class="sd">            picture (optional, List[int]):</span>
<span class="sd">                The list of picture numbers</span>

<span class="sd">        Return:</span>
<span class="sd">            list[dict]:</span>
<span class="sd">                The created user objects</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.create(</span>
<span class="sd">            ...     name=&#39;username&#39;,</span>
<span class="sd">            ...     email=&#39;test@domain.com&#39;,</span>
<span class="sd">            ...     password=&#39;user_password&#39;,</span>
<span class="sd">            ...     active=True</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">[</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
                <span class="n">dict_merge</span><span class="p">({</span>
                    <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
                    <span class="s1">&#39;email&#39;</span><span class="p">:</span> <span class="n">email</span><span class="p">,</span>
                    <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="n">password</span>
                <span class="p">},</span> <span class="n">kwargs</span><span class="p">)</span>
            <span class="p">))</span>
        <span class="p">]</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span>
            <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.info"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.info">[docs]</a>    <span class="k">def</span> <span class="nf">info</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Gets user information</span>

<span class="sd">        Return:</span>
<span class="sd">            dict:</span>
<span class="sd">                The user info object</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.info()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">UserInfoSchema</span><span class="p">()</span>
        <span class="k">return</span> <span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="s1">&#39;whoami&#39;</span><span class="p">),</span> <span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">user_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for a specific user</span>

<span class="sd">        Args:</span>
<span class="sd">            user_id (str):</span>
<span class="sd">                The user instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                the user object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.details(&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">user_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">),</span> <span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">user_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Update an existing user</span>

<span class="sd">        Args:</span>
<span class="sd">            user_id (str):</span>
<span class="sd">                The user instance identifier.</span>
<span class="sd">            name (optional, str):</span>
<span class="sd">                The name of new user.</span>
<span class="sd">            email (optional, str):</span>
<span class="sd">                The email address of the user.</span>
<span class="sd">            password (optional, str):</span>
<span class="sd">                The password for the new user.</span>
<span class="sd">            surname (optional, str):</span>
<span class="sd">                The surname of new user.</span>
<span class="sd">            department (optional, str):</span>
<span class="sd">                The department of user.</span>
<span class="sd">            biography (optional, str):</span>
<span class="sd">                The biography of user.</span>
<span class="sd">            active (optional, bool):</span>
<span class="sd">                is the user active?</span>
<span class="sd">            picture (optional, List[int]):</span>
<span class="sd">                The list of picture numbers</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The updated user object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.update(</span>
<span class="sd">            ...     user_id=&#39;1&#39;,</span>
<span class="sd">            ...     name=&#39;EDITED&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">user_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span>
            <span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.delete"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">user_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Delete an existing user</span>

<span class="sd">        Args:</span>
<span class="sd">            user_id (str):</span>
<span class="sd">                The user instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.delete(user_id=&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_delete</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">user_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.create_password"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.create_password">[docs]</a>    <span class="k">def</span> <span class="nf">create_password</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">email</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Sends an email to create new password</span>

<span class="sd">        Args:</span>
<span class="sd">            email (str):</span>
<span class="sd">                The email address of the user.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.create_password(email=&#39;test@domain.com&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;email&#39;</span><span class="p">:</span> <span class="n">email</span>
        <span class="p">}))</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="s1">&#39;forgotten-password&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.retrieve_password"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.retrieve_password">[docs]</a>    <span class="k">def</span> <span class="nf">retrieve_password</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                          <span class="n">token</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                          <span class="n">new_password</span><span class="p">:</span> <span class="nb">str</span>
                          <span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves a user password</span>

<span class="sd">        Args:</span>
<span class="sd">            token (str):</span>
<span class="sd">                user token.</span>
<span class="sd">            new_password (str):</span>
<span class="sd">                new password for user.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.retrieve_password(</span>
<span class="sd">            ...     token=&#39;token&#39;,</span>
<span class="sd">            ...     new_password=&#39;new_password&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;token&#39;</span><span class="p">:</span> <span class="n">token</span><span class="p">,</span>
            <span class="s1">&#39;newPassword&#39;</span><span class="p">:</span> <span class="n">new_password</span>
        <span class="p">}))</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="s1">&#39;retrieve-password&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.change_password"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.change_password">[docs]</a>    <span class="k">def</span> <span class="nf">change_password</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                        <span class="n">old_password</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                        <span class="n">new_password</span><span class="p">:</span> <span class="nb">str</span>
                        <span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Update a user password</span>

<span class="sd">        Args:</span>
<span class="sd">            old_password (str):</span>
<span class="sd">                old password of user.</span>
<span class="sd">            new_password (str):</span>
<span class="sd">                new password of user.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.change_password(</span>
<span class="sd">            ...     old_password=&#39;old_password&#39;,</span>
<span class="sd">            ...     new_password=&#39;new_password&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;oldPassword&#39;</span><span class="p">:</span> <span class="n">old_password</span><span class="p">,</span>
            <span class="s1">&#39;newPassword&#39;</span><span class="p">:</span> <span class="n">new_password</span>
        <span class="p">}))</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="s2">&quot;password&quot;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span></div>

<div class="viewcode-block" id="UsersAPI.update_user_roles"><a class="viewcode-back" href="../../../../tenable.ad.users.md#tenable.ad.users.api.UsersAPI.update_user_roles">[docs]</a>    <span class="k">def</span> <span class="nf">update_user_roles</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                          <span class="n">user_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                          <span class="n">roles</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="nb">int</span><span class="p">]</span>
                          <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Replace role list for user</span>

<span class="sd">        Args:</span>
<span class="sd">            user_id (str):</span>
<span class="sd">                The user instance identifier.</span>
<span class="sd">            roles (List[int]):</span>
<span class="sd">                The list of user role identifiers.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                updated user roles object</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.users.update_user_roles(</span>
<span class="sd">            ...     user_id=&#39;1&#39;,</span>
<span class="sd">            ...     roles=[1, 2, 3]</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;roles&#39;</span><span class="p">:</span> <span class="n">roles</span>
        <span class="p">}))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_put</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">user_id</span><span class="si">}</span><span class="s1">/roles&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.users.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>