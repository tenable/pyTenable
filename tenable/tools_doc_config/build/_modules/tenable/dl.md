
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.dl &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../_static/custom.css" />
    
    <script data-url_root="../../" id="documentation_options" src="../../_static/documentation_options.js"></script>
    <script src="../../_static/jquery.js"></script>
    <script src="../../_static/underscore.js"></script>
    <script src="../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../genindex.md" />
    <link rel="search" title="Search" href="../../search.md" /> 
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.dl</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.dl</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Product Downloads</span>
<span class="sd">=================</span>

<span class="sd">.. autoclass:: Downloads</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">tenable.base.platform</span> <span class="kn">import</span> <span class="n">APIPlatform</span>
<span class="kn">from</span> <span class="nn">box</span> <span class="kn">import</span> <span class="n">BoxList</span>
<span class="kn">from</span> <span class="nn">io</span> <span class="kn">import</span> <span class="n">BytesIO</span>
<span class="kn">import</span> <span class="nn">os</span><span class="o">,</span> <span class="nn">warnings</span>

<div class="viewcode-block" id="Downloads"><a class="viewcode-back" href="../../tenable.dl.md#tenable.dl.Downloads">[docs]</a><span class="k">class</span> <span class="nc">Downloads</span><span class="p">(</span><span class="n">APIPlatform</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    The Downloads object is the primary interaction point for users to</span>
<span class="sd">    interface with Downloads API via the pyTenable library.  All of the API</span>
<span class="sd">    endpoint classes that have been written will be grafted onto this class.</span>

<span class="sd">    Args:</span>
<span class="sd">        api_token (str, optional):</span>
<span class="sd">            The user&#39;s API access key for Tenable.io  If an access key isn&#39;t</span>
<span class="sd">            specified, then the library will attempt to read the environment</span>
<span class="sd">            variable ``TDL_API_TOKEN`` to acquire the key.</span>
<span class="sd">        retries (int, optional):</span>
<span class="sd">            The number of retries to make before failing a request.  The</span>
<span class="sd">            default is ``5``.</span>
<span class="sd">        backoff (float, optional):</span>
<span class="sd">            If a 429 response is returned, how much do we want to backoff</span>
<span class="sd">            if the response didn&#39;t send a Retry-After header.  The default</span>
<span class="sd">            backoff is ``1`` second.</span>
<span class="sd">        vendor (str, optional):</span>
<span class="sd">            The vendor name for the User-Agent string.</span>
<span class="sd">        product (str, optional):</span>
<span class="sd">            The product name for the User-Agent string.</span>
<span class="sd">        build (str, optional):</span>
<span class="sd">            The version or build identifier for the User-Agent string.</span>
<span class="sd">        timeout (int, optional):</span>
<span class="sd">            The connection timeout parameter informing the library how long to</span>
<span class="sd">            wait in seconds for a stalled response before terminating the</span>
<span class="sd">            connection.  If unspecified, the default is 120 seconds.</span>

<span class="sd">    Examples:</span>
<span class="sd">        Basic Example:</span>

<span class="sd">        &gt;&gt;&gt; from tenable.dl import Downloads</span>
<span class="sd">        &gt;&gt;&gt; dl = Downloads(api_token=&#39;API_TOKEN&#39;)</span>

<span class="sd">        Example with proper identification:</span>

<span class="sd">        &gt;&gt;&gt; dl = Downloads(&#39;API_TOKEN&#39;,</span>
<span class="sd">        &gt;&gt;&gt;     vendor=&#39;Company Name&#39;,</span>
<span class="sd">        &gt;&gt;&gt;     product=&#39;My Awesome Widget&#39;,</span>
<span class="sd">        &gt;&gt;&gt;     build=&#39;1.0.0&#39;)</span>

<span class="sd">        Example with proper identification leveraging environment variables for</span>
<span class="sd">        access and secret keys:</span>

<span class="sd">        &gt;&gt;&gt; dl = Downloads(</span>
<span class="sd">        &gt;&gt;&gt;     vendor=&#39;Company Name&#39;, product=&#39;Widget&#39;, build=&#39;1.0.0&#39;)</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">_box</span> <span class="o">=</span> <span class="kc">True</span>
    <span class="n">_env_base</span> <span class="o">=</span> <span class="s1">&#39;TDL&#39;</span>
    <span class="n">_url</span> <span class="o">=</span> <span class="s1">&#39;https://www.tenable.com&#39;</span>
    <span class="n">_base_path</span> <span class="o">=</span> <span class="s1">&#39;downloads/api/v2&#39;</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">api_token</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">api_token</span><span class="p">:</span>
            <span class="n">api_token</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">&#39;</span><span class="si">{}</span><span class="s1">_API_TOKEN&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="p">))</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;api_token&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">api_token</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

    <span class="k">def</span> <span class="nf">_authenticate</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Authentication method for Downloads API</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;api_token&#39;</span><span class="p">):</span>
            <span class="n">warnings</span><span class="o">.</span><span class="n">warn</span><span class="p">(</span><span class="s1">&#39;Starting an unauthenticated session&#39;</span><span class="p">)</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_log</span><span class="o">.</span><span class="n">warning</span><span class="p">(</span><span class="s1">&#39;Starting an unauthenticated session.&#39;</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_session</span><span class="o">.</span><span class="n">headers</span><span class="o">.</span><span class="n">update</span><span class="p">({</span>
                <span class="s1">&#39;Authorization&#39;</span><span class="p">:</span> <span class="s1">&#39;Bearer </span><span class="si">{token}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
                    <span class="n">token</span><span class="o">=</span><span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;api_token&#39;</span><span class="p">)</span>
                <span class="p">)</span>
            <span class="p">})</span>

<div class="viewcode-block" id="Downloads.list"><a class="viewcode-back" href="../../tenable.dl.md#tenable.dl.Downloads.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Lists the available content pages.</span>

<span class="sd">        :devportal:`API Endpoint Documentation &lt;get_pages&gt;`</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                The list of page resources.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; pages = dl.list()</span>
<span class="sd">            &gt;&gt;&gt; for page in pages:</span>
<span class="sd">            ...     pprint(page)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;pages&#39;</span><span class="p">,</span> <span class="n">box</span><span class="o">=</span><span class="n">BoxList</span><span class="p">)</span></div>

<div class="viewcode-block" id="Downloads.details"><a class="viewcode-back" href="../../tenable.dl.md#tenable.dl.Downloads.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">page</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the specific download items for the page requested.</span>

<span class="sd">        :devportal:`API Endpoint Documentation &lt;get_pages-slug&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            page (str): The name of the page to request.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The page details.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; details = dl.details(&#39;nessus&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;pages/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">page</span><span class="p">))</span></div>

<div class="viewcode-block" id="Downloads.download"><a class="viewcode-back" href="../../tenable.dl.md#tenable.dl.Downloads.download">[docs]</a>    <span class="k">def</span> <span class="nf">download</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">page</span><span class="p">,</span> <span class="n">package</span><span class="p">,</span> <span class="n">fobj</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the requested package and downloads the file.</span>

<span class="sd">        :devportal:`API Endpoint Documentation &lt;get_pages-slug-files-file&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            page (str): The name of the page</span>
<span class="sd">            package (str): The package filename</span>
<span class="sd">            fobj (FileObject, optional):</span>
<span class="sd">                The file-like object to write the package to.  If nothing is</span>
<span class="sd">                specified, then a BytesIO object will be used.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`FileObject`:</span>
<span class="sd">                The binary package</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;Nessus-latest.x86_64.rpm&#39;, &#39;wb&#39;) as pkgfile:</span>
<span class="sd">            ...     dl.download(&#39;nessus&#39;,</span>
<span class="sd">            ...         &#39;Nessus-8.3.0-es7.x86_64.rpm&#39;, pkgfile)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">fobj</span><span class="p">:</span>
            <span class="n">fobj</span> <span class="o">=</span> <span class="n">BytesIO</span><span class="p">()</span>

        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
            <span class="s1">&#39;pages/</span><span class="si">{}</span><span class="s1">/files/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">page</span><span class="p">,</span> <span class="n">package</span><span class="p">),</span> <span class="n">stream</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">box</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>

        <span class="c1"># Lets stream the file into the file-like object...</span>
        <span class="k">for</span> <span class="n">chunk</span> <span class="ow">in</span> <span class="n">resp</span><span class="o">.</span><span class="n">iter_content</span><span class="p">(</span><span class="n">chunk_size</span><span class="o">=</span><span class="mi">1024</span><span class="p">):</span>
            <span class="k">if</span> <span class="n">chunk</span><span class="p">:</span>
                <span class="n">fobj</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">chunk</span><span class="p">)</span>
        <span class="n">fobj</span><span class="o">.</span><span class="n">seek</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span>
        <span class="n">resp</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>

        <span class="c1"># Lastly lets return the FileObject to the caller.</span>
        <span class="k">return</span> <span class="n">fobj</span></div></div>
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
          <a href="../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.dl</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>