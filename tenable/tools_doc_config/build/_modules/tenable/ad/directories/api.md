
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.directories.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.directories.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.directories.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Directory</span>
<span class="sd">=========</span>

<span class="sd">Methods described in this section relate to the the directory API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.directories``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: DirectoriesAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">INCLUDE</span>
<span class="kn">from</span> <span class="nn">restfly.utils</span> <span class="kn">import</span> <span class="n">dict_clean</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">.schema</span> <span class="kn">import</span> <span class="n">DirectorySchema</span>


<div class="viewcode-block" id="DirectoriesAPI"><a class="viewcode-back" href="../../../../tenable.ad.directories.md#tenable.ad.directories.api.DirectoriesAPI">[docs]</a><span class="k">class</span> <span class="nc">DirectoriesAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;directories&#39;</span>

<div class="viewcode-block" id="DirectoriesAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.directories.md#tenable.ad.directories.api.DirectoriesAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves all directory instances.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                The list of directory objects</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.directories.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">DirectorySchema</span><span class="p">(</span><span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="DirectoriesAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.directories.md#tenable.ad.directories.api.DirectoriesAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">infrastructure_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">ip</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">dns</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new directory instance.</span>

<span class="sd">        Args:</span>
<span class="sd">            infrastructure_id (int):</span>
<span class="sd">                The infrastructure object to bind this directory to.</span>
<span class="sd">            name (str):</span>
<span class="sd">                Name of the directory instance.</span>
<span class="sd">            ip (str):</span>
<span class="sd">                The IP Address of the directory server.</span>
<span class="sd">            dns (str):</span>
<span class="sd">                The DNS domain that this directory is tied to.</span>
<span class="sd">            directory_type (optional, str):</span>
<span class="sd">                The directory&#39;s type.</span>
<span class="sd">            ldap_port (optional, str):</span>
<span class="sd">                The port number associated to the LDAP service on the</span>
<span class="sd">                directory server.</span>
<span class="sd">            global_catalog_port (optional, str):</span>
<span class="sd">                The port number associated to the Global Catalog service</span>
<span class="sd">                running on the directory server.</span>
<span class="sd">            smb_port (optional, str):</span>
<span class="sd">                The port number associated to the Server Messaging</span>
<span class="sd">                Block (SMB) service running on the directory server.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The created directory instance.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.directories.create(</span>
<span class="sd">            ...     infrastructure_id=1,</span>
<span class="sd">            ...     name=&#39;ExampleServer&#39;,</span>
<span class="sd">            ...     ip=&#39;172.16.0.1&#39;,</span>
<span class="sd">            ...     directory_type=&#39;????&#39;,</span>
<span class="sd">            ...     dns=&#39;company.tld&#39;,</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">DirectorySchema</span><span class="p">(</span><span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">[</span><span class="n">schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="n">dict_clean</span><span class="p">({</span>
                <span class="s1">&#39;infrastructureId&#39;</span><span class="p">:</span> <span class="n">infrastructure_id</span><span class="p">,</span>
                <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
                <span class="s1">&#39;ip&#39;</span><span class="p">:</span> <span class="n">ip</span><span class="p">,</span>
                <span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;directory_type&#39;</span><span class="p">),</span>
                <span class="s1">&#39;dns&#39;</span><span class="p">:</span> <span class="n">dns</span><span class="p">,</span>
                <span class="s1">&#39;ldapPort&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;ldap_port&#39;</span><span class="p">),</span>
                <span class="s1">&#39;globalCatalogPort&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;global_catalog_port&#39;</span><span class="p">),</span>
                <span class="s1">&#39;smbPort&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;smb_port&#39;</span><span class="p">)</span>
            <span class="p">})</span>
        <span class="p">))]</span>
        <span class="k">return</span> <span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="DirectoriesAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.directories.md#tenable.ad.directories.api.DirectoriesAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">directory_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for a specific directory instance.</span>

<span class="sd">        Args:</span>
<span class="sd">            directory_id (str): The directory instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                the directory object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.directories.details(directory_id=&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">DirectorySchema</span><span class="p">(</span><span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">directory_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">))</span></div>

<div class="viewcode-block" id="DirectoriesAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.directories.md#tenable.ad.directories.api.DirectoriesAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">infrastructure_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">directory_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Updates the directory instance based on infrastrcture_id and</span>
<span class="sd">        directory_id.</span>

<span class="sd">        Args:</span>
<span class="sd">            infrastructure_id (int):</span>
<span class="sd">                The infrastructure instance identifier.</span>
<span class="sd">            directory_id (int):</span>
<span class="sd">                The directory instance identifier.</span>
<span class="sd">            name (optional, str):</span>
<span class="sd">                Name of the directory instance.</span>
<span class="sd">            ip (optional, str):</span>
<span class="sd">                The IP Address of the directory server.</span>
<span class="sd">            directory_type (optional, str):</span>
<span class="sd">                The directory&#39;s type.</span>
<span class="sd">            dns (optional, str):</span>
<span class="sd">                The DNS domain that this directory is tied to.</span>
<span class="sd">            ldap_port (optional, int):</span>
<span class="sd">                The port number associated to the LDAP service on the</span>
<span class="sd">                directory server.</span>
<span class="sd">            global_catalog_port (optional, str):</span>
<span class="sd">                The port number associated to the Global Catalog service</span>
<span class="sd">                running on the directory server.</span>
<span class="sd">            smb_port (optional, str):</span>
<span class="sd">                The port number associated to the Server Messaging</span>
<span class="sd">                Block (SMB) service running on the directory server.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The updated directory object.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.directories.update(</span>
<span class="sd">            ...     infrastructure_id=2,</span>
<span class="sd">            ...     directory_id=9,</span>
<span class="sd">            ...     name=&#39;updated_new_name&#39;</span>
<span class="sd">            ...     )</span>

<span class="sd">            &gt;&gt;&gt; tad.directories.update(</span>
<span class="sd">            ...     infrastructure_id=2,</span>
<span class="sd">            ...     directory_id=9,</span>
<span class="sd">            ...     name=&#39;updated_new_name&#39;,</span>
<span class="sd">            ...     ldap_port=390</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">DirectorySchema</span><span class="p">(</span><span class="n">unknown</span><span class="o">=</span><span class="n">INCLUDE</span><span class="p">)</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="n">schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">((</span><span class="sa">f</span><span class="s1">&#39;infrastructures/</span><span class="si">{</span><span class="n">infrastructure_id</span><span class="si">}</span><span class="s1">&#39;</span>
                             <span class="sa">f</span><span class="s1">&#39;/directories/</span><span class="si">{</span><span class="n">directory_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">),</span>
                            <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>

<div class="viewcode-block" id="DirectoriesAPI.delete"><a class="viewcode-back" href="../../../../tenable.ad.directories.md#tenable.ad.directories.api.DirectoriesAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">infrastructure_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span> <span class="n">directory_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Deletes the directory instance.</span>

<span class="sd">        Args:</span>
<span class="sd">            infrastructure_id (int):</span>
<span class="sd">                The infrastructure instance identifier.</span>
<span class="sd">            directory_id (int):</span>
<span class="sd">                The directory instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.directories.delete(</span>
<span class="sd">            ...     infrastructure_id=2,</span>
<span class="sd">            ...     directory_id=&#39;12&#39;</span>
<span class="sd">            ...     )</span>

<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">((</span><span class="sa">f</span><span class="s1">&#39;infrastructures/</span><span class="si">{</span><span class="n">infrastructure_id</span><span class="si">}</span><span class="s1">&#39;</span>
                          <span class="sa">f</span><span class="s1">&#39;/directories/</span><span class="si">{</span><span class="n">directory_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">))</span></div></div>

    <span class="c1"># NOTE: Get All Directories for a Given Infrastructure is located within</span>
    <span class="c1">#       the infrastructures module.</span>
    <span class="c1">#</span>
    <span class="c1"># NOTE: Get Directory instance by id is located within the infrastructures</span>
    <span class="c1">#       module.</span>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.directories.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>