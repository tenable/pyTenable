
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Tenable.sc</span>
<span class="sd">==========</span>

<span class="sd">.. note::</span>
<span class="sd">    Please refer to the common themes section for TenableSC for details on how</span>
<span class="sd">    these methods are written from an overall concept.  Not all attributes are</span>
<span class="sd">    explicitly documented, only the ones that pyTenable is augmenting,</span>
<span class="sd">    validating, or modifying.  For a complete listing of the attributes that can</span>
<span class="sd">    be passed to most APIs, refer to the official API documentation that each</span>
<span class="sd">    method calls, which is conveniently linked in each method&#39;s docs.</span>

<span class="sd">.. autoclass:: TenableSC</span>
<span class="sd">   :members:</span>


<span class="sd">.. toctree::</span>
<span class="sd">    :hidden:</span>
<span class="sd">    :glob:</span>

<span class="sd">    base</span>
<span class="sd">    accept_risks</span>
<span class="sd">    alerts</span>
<span class="sd">    analysis</span>
<span class="sd">    asset_lists</span>
<span class="sd">    audit_files</span>
<span class="sd">    credentials</span>
<span class="sd">    current</span>
<span class="sd">    feeds</span>
<span class="sd">    files</span>
<span class="sd">    groups</span>
<span class="sd">    organizations</span>
<span class="sd">    plugins</span>
<span class="sd">    policies</span>
<span class="sd">    queries</span>
<span class="sd">    recast_risks</span>
<span class="sd">    repositories</span>
<span class="sd">    roles</span>
<span class="sd">    scan_instances</span>
<span class="sd">    scan_zones</span>
<span class="sd">    scanners</span>
<span class="sd">    scans</span>
<span class="sd">    status</span>
<span class="sd">    system</span>
<span class="sd">    users</span>

<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">import</span> <span class="nn">warnings</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Optional</span>
<span class="kn">from</span> <span class="nn">semver</span> <span class="kn">import</span> <span class="n">VersionInfo</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">APIError</span><span class="p">,</span> <span class="ne">ConnectionError</span>
<span class="kn">from</span> <span class="nn">tenable.base.platform</span> <span class="kn">import</span> <span class="n">APIPlatform</span>
<span class="kn">from</span> <span class="nn">.accept_risks</span> <span class="kn">import</span> <span class="n">AcceptRiskAPI</span>
<span class="kn">from</span> <span class="nn">.alerts</span> <span class="kn">import</span> <span class="n">AlertAPI</span>
<span class="kn">from</span> <span class="nn">.analysis</span> <span class="kn">import</span> <span class="n">AnalysisAPI</span>
<span class="kn">from</span> <span class="nn">.asset_lists</span> <span class="kn">import</span> <span class="n">AssetListAPI</span>
<span class="kn">from</span> <span class="nn">.audit_files</span> <span class="kn">import</span> <span class="n">AuditFileAPI</span>
<span class="kn">from</span> <span class="nn">.credentials</span> <span class="kn">import</span> <span class="n">CredentialAPI</span>
<span class="kn">from</span> <span class="nn">.current</span> <span class="kn">import</span> <span class="n">CurrentSessionAPI</span>
<span class="kn">from</span> <span class="nn">.files</span> <span class="kn">import</span> <span class="n">FileAPI</span>
<span class="kn">from</span> <span class="nn">.feeds</span> <span class="kn">import</span> <span class="n">FeedAPI</span>
<span class="kn">from</span> <span class="nn">.groups</span> <span class="kn">import</span> <span class="n">GroupAPI</span>
<span class="kn">from</span> <span class="nn">.organizations</span> <span class="kn">import</span> <span class="n">OrganizationAPI</span>
<span class="kn">from</span> <span class="nn">.plugins</span> <span class="kn">import</span> <span class="n">PluginAPI</span>
<span class="kn">from</span> <span class="nn">.policies</span> <span class="kn">import</span> <span class="n">ScanPolicyAPI</span>
<span class="kn">from</span> <span class="nn">.queries</span> <span class="kn">import</span> <span class="n">QueryAPI</span>
<span class="kn">from</span> <span class="nn">.recast_risks</span> <span class="kn">import</span> <span class="n">RecastRiskAPI</span>
<span class="kn">from</span> <span class="nn">.repositories</span> <span class="kn">import</span> <span class="n">RepositoryAPI</span>
<span class="kn">from</span> <span class="nn">.roles</span> <span class="kn">import</span> <span class="n">RoleAPI</span>
<span class="kn">from</span> <span class="nn">.scanners</span> <span class="kn">import</span> <span class="n">ScannerAPI</span>
<span class="kn">from</span> <span class="nn">.scans</span> <span class="kn">import</span> <span class="n">ScanAPI</span>
<span class="kn">from</span> <span class="nn">.scan_instances</span> <span class="kn">import</span> <span class="n">ScanResultAPI</span>
<span class="kn">from</span> <span class="nn">.scan_zones</span> <span class="kn">import</span> <span class="n">ScanZoneAPI</span>
<span class="kn">from</span> <span class="nn">.status</span> <span class="kn">import</span> <span class="n">StatusAPI</span>
<span class="kn">from</span> <span class="nn">.system</span> <span class="kn">import</span> <span class="n">SystemAPI</span>
<span class="kn">from</span> <span class="nn">.users</span> <span class="kn">import</span> <span class="n">UserAPI</span>


<div class="viewcode-block" id="TenableSC"><a class="viewcode-back" href="../../tenable.sc.md#tenable.sc.TenableSC">[docs]</a><span class="k">class</span> <span class="nc">TenableSC</span><span class="p">(</span><span class="n">APIPlatform</span><span class="p">):</span>  <span class="c1"># noqa PLR0904</span>
    <span class="sd">&#39;&#39;&#39;TenableSC API Wrapper</span>
<span class="sd">    The Tenable.sc object is the primary interaction point for users to</span>
<span class="sd">    interface with Tenable.sc via the pyTenable library.  All of the API</span>
<span class="sd">    endpoint classes that have been written will be grafted onto this class.</span>

<span class="sd">    Args:</span>
<span class="sd">        host (str):</span>
<span class="sd">            The address of the Tenable.sc instance to connect to.  (NOTE: The</span>
<span class="sd">            `hos`t parameter will be deprecated in favor of the `url` parameter</span>
<span class="sd">            in future releases).</span>
<span class="sd">        access_key (str, optional):</span>
<span class="sd">            The API access key to use for sessionless authentication.</span>
<span class="sd">        adapter (requests.Adaptor, optional):</span>
<span class="sd">            If a requests session adaptor is needed to ensure connectivity</span>
<span class="sd">            to the Tenable.sc host, one can be provided here.</span>
<span class="sd">        backoff (float, optional):</span>
<span class="sd">            If a 429 response is returned, how much do we want to backoff</span>
<span class="sd">            if the response didn&#39;t send a Retry-After header.  The default</span>
<span class="sd">            backoff is ``1`` second.</span>
<span class="sd">        cert (tuple, optional):</span>
<span class="sd">            The client-side SSL certificate to use for authentication.  This</span>
<span class="sd">            format could be either a tuple or a string pointing to the</span>
<span class="sd">            certificate.  For more details, please refer to the</span>
<span class="sd">            `Requests Client-Side Certificates`_ documentation.</span>
<span class="sd">        password (str, optional):</span>
<span class="sd">            The password to use for session authentication.</span>
<span class="sd">        port (int, optional):</span>
<span class="sd">            The port number to connect to on the specified host.  The</span>
<span class="sd">            default is port ``443``.  (NOTE: The `port` parameter will be</span>
<span class="sd">            deprecated in favor of the unified `url` parameter in future</span>
<span class="sd">            releases).</span>
<span class="sd">        retries (int, optional):</span>
<span class="sd">            The number of retries to make before failing a request.  The</span>
<span class="sd">            default is ``5``.</span>
<span class="sd">        scheme (str, optional):</span>
<span class="sd">            What HTTP scheme should be used for URI path construction.  The</span>
<span class="sd">            default is ``https``.  (NOTE: The `scheme` parameter will be</span>
<span class="sd">            deprecated in favor of the unified `url` parameter in future</span>
<span class="sd">            releases).</span>
<span class="sd">        secret_key (str, optional):</span>
<span class="sd">            The API secret key to use for sessionless authentication.</span>
<span class="sd">        session (requests.Session, optional):</span>
<span class="sd">            If a requests Session is provided, the provided session will be</span>
<span class="sd">            used instead of constructing one during initialization.</span>
<span class="sd">        ssl_verify (bool, optional):</span>
<span class="sd">            Should the SSL certificate on the Tenable.sc instance be verified?</span>
<span class="sd">            Default is False.</span>
<span class="sd">        username (str, optional):</span>
<span class="sd">            The username to use for session authentication.</span>
<span class="sd">        timeout (int, optional):</span>
<span class="sd">            The connection timeout parameter informing the library how long to</span>
<span class="sd">            wait in seconds for a stalled response before terminating the</span>
<span class="sd">            connection.  If unspecified, the default is 300 seconds.</span>


<span class="sd">    Examples:</span>
<span class="sd">        A direct connection to Tenable.sc:</span>

<span class="sd">        &gt;&gt;&gt; from tenable.sc import TenableSC</span>
<span class="sd">        &gt;&gt;&gt; sc = TenableSC(&#39;sc.company.tld&#39;)</span>

<span class="sd">        A connection to Tenable.sc using SSL certificates:</span>

<span class="sd">        &gt;&gt;&gt; sc = TenableSC(&#39;sc.company.tld&#39;,</span>
<span class="sd">        ...     cert=(&#39;/path/client.cert&#39;, &#39;/path/client.key&#39;))</span>

<span class="sd">        Using an adaptor to use a passworded certificate (via the immensely</span>
<span class="sd">        useful `requests_pkcs12`_ adaptor):</span>

<span class="sd">        &gt;&gt;&gt; from requests_pkcs12 import Pkcs12Adapter</span>
<span class="sd">        &gt;&gt;&gt; adapter = Pkcs12Adapter(</span>
<span class="sd">        ...     pkcs12_filename=&#39;certificate.p12&#39;,</span>
<span class="sd">        ...     pkcs12_password=&#39;omgwtfbbq!&#39;)</span>
<span class="sd">        &gt;&gt;&gt; sc = TenableSC(&#39;sc.company.tld&#39;, adapter=adapter)</span>

<span class="sd">        Using API Keys to communicate to Tenable.sc:</span>

<span class="sd">        &gt;&gt;&gt; sc = TenableSC(&#39;sc.company.tld&#39;,</span>
<span class="sd">        ...     access_key=&#39;key&#39;,</span>
<span class="sd">        ...     secret_key=&#39;key&#39;</span>
<span class="sd">        ... )</span>

<span class="sd">        Using context management to handle</span>

<span class="sd">    For more information, please See Tenable&#39;s `SC API documentation`_ and</span>
<span class="sd">    the `SC API Best Practices Guide`_.</span>

<span class="sd">    .. _SC API documentation:</span>
<span class="sd">        https://docs.tenable.com/sccv/api/index.html</span>
<span class="sd">    .. _SC API Best Practices Guide:</span>
<span class="sd">        https://docs.tenable.com/sccv/api_best_practices/Content/ScApiBestPractices/AboutScApiBestPrac.htm</span>
<span class="sd">    .. _Requests Client-Side Certificates:</span>
<span class="sd">        http://docs.python-requests.org/en/master/user/advanced/#client-side-certificates</span>
<span class="sd">    .. _requests_pkcs12:</span>
<span class="sd">        https://github.com/m-click/requests_pkcs12</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">_env_base</span> <span class="o">=</span> <span class="s1">&#39;TSC&#39;</span>
    <span class="n">_base_path</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="s1">&#39;rest&#39;</span>
    <span class="n">_error_map</span> <span class="o">=</span> <span class="p">{</span><span class="mi">403</span><span class="p">:</span> <span class="n">APIError</span><span class="p">}</span>
    <span class="n">_restricted_paths</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;token&#39;</span><span class="p">,</span> <span class="s1">&#39;credential&#39;</span><span class="p">]</span>
    <span class="n">_timeout</span> <span class="o">=</span> <span class="mi">300</span>
    <span class="n">_ssl_verify</span> <span class="o">=</span> <span class="kc">False</span>
    <span class="n">_version</span> <span class="o">=</span> <span class="kc">None</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>  <span class="c1"># noqa: PLR0913</span>
                 <span class="n">host</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
                 <span class="n">access_key</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
                 <span class="n">secret_key</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
                 <span class="o">**</span><span class="n">kwargs</span>
                 <span class="p">):</span>
        <span class="c1"># As we will always be passing a URL to the APISession class, we will</span>
        <span class="c1"># want to construct a URL that APISession (and further requests)</span>
        <span class="c1"># understands.</span>
        <span class="k">if</span> <span class="n">host</span><span class="p">:</span>
            <span class="n">warnings</span><span class="o">.</span><span class="n">warn</span><span class="p">(</span><span class="s1">&#39;The &quot;host&quot;, &quot;port&quot;, and &quot;scheme&quot; parameters are &#39;</span>
                          <span class="s1">&#39;deprecated and will be removed from the TenableSC &#39;</span>
                          <span class="s1">&#39;class in version 2.0.&#39;</span><span class="p">,</span>
                          <span class="ne">DeprecationWarning</span>
                          <span class="p">)</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;url&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;scheme&quot;</span><span class="p">,</span> <span class="s2">&quot;https&quot;</span><span class="p">)</span><span class="si">}</span><span class="s1">://&#39;</span>
                             <span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">host</span><span class="si">}</span><span class="s1">:</span><span class="si">{</span><span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;port&quot;</span><span class="p">,</span> <span class="mi">443</span><span class="p">)</span><span class="si">}</span><span class="s1">&#39;</span>
                             <span class="p">)</span>
        <span class="k">if</span> <span class="n">access_key</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;access_key&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">access_key</span>
        <span class="k">if</span> <span class="n">secret_key</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;secret_key&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">secret_key</span>

        <span class="c1"># Now lets pass the relevant parts off to the APISession&#39;s constructor</span>
        <span class="c1"># to make sure we have everything lined up as we expect.</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

    <span class="k">def</span> <span class="fm">__enter__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="bp">self</span>

    <span class="k">def</span> <span class="fm">__exit__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">exc_type</span><span class="p">,</span> <span class="n">exc_value</span><span class="p">,</span> <span class="n">exc_traceback</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">logout</span><span class="p">()</span>

    <span class="k">def</span> <span class="nf">_resp_error_check</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">response</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;stream&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">):</span>
            <span class="k">try</span><span class="p">:</span>
                <span class="n">data</span> <span class="o">=</span> <span class="n">response</span><span class="o">.</span><span class="n">json</span><span class="p">()</span>
                <span class="k">if</span> <span class="n">data</span><span class="p">[</span><span class="s1">&#39;error_code&#39;</span><span class="p">]:</span>
                    <span class="k">raise</span> <span class="n">APIError</span><span class="p">(</span><span class="n">response</span><span class="p">)</span>
            <span class="k">except</span> <span class="ne">ValueError</span><span class="p">:</span>
                <span class="k">pass</span>
        <span class="k">return</span> <span class="n">response</span>

    <span class="k">def</span> <span class="nf">_key_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">access_key</span><span class="p">,</span> <span class="n">secret_key</span><span class="p">):</span>
        <span class="c1"># if we can pull a version, check to see that the version is at least</span>
        <span class="c1"># 5.13, which is the minimum version of SC that supports API Keys.  If</span>
        <span class="c1"># we cant pull a version, then we will assume it&#39;s ok.</span>
        <span class="k">if</span> <span class="p">(</span><span class="ow">not</span> <span class="bp">self</span><span class="o">.</span><span class="n">version</span>
            <span class="ow">or</span> <span class="n">VersionInfo</span><span class="o">.</span><span class="n">parse</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">version</span><span class="p">)</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="s1">&#39;&gt;=5.13.0&#39;</span><span class="p">)</span>
        <span class="p">):</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_session</span><span class="o">.</span><span class="n">headers</span><span class="o">.</span><span class="n">update</span><span class="p">({</span>
                <span class="s1">&#39;X-APIKey&#39;</span><span class="p">:</span> <span class="sa">f</span><span class="s1">&#39;accessKey=</span><span class="si">{</span><span class="n">access_key</span><span class="si">}</span><span class="s1">; secretKey=</span><span class="si">{</span><span class="n">secret_key</span><span class="si">}</span><span class="s1">&#39;</span>
            <span class="p">})</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">=</span> <span class="s1">&#39;keys&#39;</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="k">raise</span> <span class="ne">ConnectionError</span><span class="p">(</span>
                   <span class="sa">f</span><span class="s1">&#39;API Keys not supported on Tenable.sc </span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">version</span><span class="si">}</span><span class="s1">&#39;</span>
                <span class="p">)</span>

    <span class="k">def</span> <span class="nf">_session_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">password</span><span class="p">):</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;token&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;username&#39;</span><span class="p">:</span> <span class="n">username</span><span class="p">,</span>
            <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="n">password</span>
        <span class="p">})</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">=</span> <span class="s1">&#39;user&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_session</span><span class="o">.</span><span class="n">headers</span><span class="o">.</span><span class="n">update</span><span class="p">({</span>
            <span class="s1">&#39;X-SecurityCenter&#39;</span><span class="p">:</span> <span class="nb">str</span><span class="p">(</span><span class="n">resp</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="s1">&#39;token&#39;</span><span class="p">]),</span>
            <span class="s1">&#39;TNS_SESSIONID&#39;</span><span class="p">:</span> <span class="nb">str</span><span class="p">(</span><span class="n">resp</span><span class="o">.</span><span class="n">headers</span><span class="p">[</span><span class="s1">&#39;Set-Cookie&#39;</span><span class="p">])[</span><span class="mi">14</span><span class="p">:</span><span class="mi">46</span><span class="p">]</span>
        <span class="p">})</span>

    <span class="k">def</span> <span class="nf">_deauthenticate</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>  <span class="c1"># noqa PLW0221</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">_deauthenticate</span><span class="p">(</span><span class="n">path</span><span class="o">=</span><span class="s1">&#39;token&#39;</span><span class="p">)</span>

<div class="viewcode-block" id="TenableSC.login"><a class="viewcode-back" href="../../tenable.sc.md#tenable.sc.TenableSC.login">[docs]</a>    <span class="k">def</span> <span class="nf">login</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">username</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">password</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span>
              <span class="n">access_key</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">secret_key</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Logs the user into Tenable.sc</span>

<span class="sd">        Args:</span>
<span class="sd">            username (str, optional): Username</span>
<span class="sd">            password (str, optional): Password</span>
<span class="sd">            access_key (str, optional): API Access Key</span>
<span class="sd">            secret_key (str, optional): API Secret Key</span>

<span class="sd">        Returns:</span>
<span class="sd">            None</span>

<span class="sd">        Examples:</span>

<span class="sd">            Using a username &amp;&amp; password:</span>

<span class="sd">            &gt;&gt;&gt; sc = TenableSC(&#39;127.0.0.1&#39;, port=8443)</span>
<span class="sd">            &gt;&gt;&gt; sc.login(&#39;username&#39;, &#39;password&#39;)</span>

<span class="sd">            Using API Keys:</span>

<span class="sd">            &gt;&gt;&gt; sc = TenableSC(&#39;127.0.0.1&#39;, port=8443)</span>
<span class="sd">            &gt;&gt;&gt; sc.login(access_key=&#39;ACCESSKEY&#39;, secret_key=&#39;SECRETKEY&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_authenticate</span><span class="p">(</span><span class="o">**</span><span class="p">{</span>
            <span class="s1">&#39;username&#39;</span><span class="p">:</span> <span class="n">username</span><span class="p">,</span>
            <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="n">password</span><span class="p">,</span>
            <span class="s1">&#39;access_key&#39;</span><span class="p">:</span> <span class="n">access_key</span><span class="p">,</span>
            <span class="s1">&#39;secret_key&#39;</span><span class="p">:</span> <span class="n">secret_key</span>
        <span class="p">})</span></div>

<div class="viewcode-block" id="TenableSC.logout"><a class="viewcode-back" href="../../tenable.sc.md#tenable.sc.TenableSC.logout">[docs]</a>    <span class="k">def</span> <span class="nf">logout</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Logs out of Tenable.sc and resets the session.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.logout()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_deauthenticate</span><span class="p">()</span></div>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">version</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="bp">self</span><span class="o">.</span><span class="n">_version</span><span class="p">:</span>
            <span class="c1"># We will attempt to pull the version number from the system</span>
            <span class="c1"># details method.  If we get an APRError response, then we will</span>
            <span class="c1"># simply pass through.</span>
            <span class="k">try</span><span class="p">:</span>
                <span class="n">version</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">system</span><span class="o">.</span><span class="n">details</span><span class="p">()</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;version&#39;</span><span class="p">)</span>
            <span class="k">except</span> <span class="n">APIError</span><span class="p">:</span>
                <span class="k">pass</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_version</span> <span class="o">=</span> <span class="n">version</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_version</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">accept_risks</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Accept Risks APIs &lt;accept_risks&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AcceptRiskAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">alerts</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Alerts APIs &lt;alerts&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AlertAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">analysis</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Analysis APIs &lt;analysis&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AnalysisAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">asset_lists</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Asset Lists APIs &lt;asset_lists&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AssetListAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">audit_files</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Audit Files APIs &lt;audit_files&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AuditFileAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">credentials</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Credentials APIs &lt;credentials&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">CredentialAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">current</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Current Session APIs &lt;current&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">CurrentSessionAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">feeds</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Feeds APIs &lt;feeds&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">FeedAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">files</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Files APIs &lt;files&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">FileAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">groups</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Groups APIs &lt;groups&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">GroupAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">organizations</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Organization APIs &lt;organizations&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">OrganizationAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">plugins</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Plugins APIs &lt;plugins&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">PluginAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">policies</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Policies APIs &lt;policies&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">ScanPolicyAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">queries</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Queries APIs &lt;queries&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">QueryAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">recast_risks</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Recast Risks APIs &lt;recast_risks&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">RecastRiskAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">repositories</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Repositories APIs &lt;repositories&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">RepositoryAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">roles</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Roles APIs &lt;roles&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">RoleAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">scanners</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Scanners APIs &lt;scanners&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">ScannerAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">scans</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Scans APIs &lt;scans&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">ScanAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">scan_instances</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Scan Instances APIs &lt;scan_instances&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">ScanResultAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">scan_zones</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Scan Zones APIs &lt;scan_zones&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">ScanZoneAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">status</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Status APIs &lt;status&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">StatusAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">system</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc System APIs &lt;system&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">SystemAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">users</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.sc Users APIs &lt;users&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">UserAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>