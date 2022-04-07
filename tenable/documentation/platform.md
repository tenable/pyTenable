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
        <li class="nav-item nav-item-this"><a href="">tenable.base.platform</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.base.platform</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Base Platform</span>
<span class="sd">=============</span>
<span class="sd">The APIPlatform class is the base class that all platform packages will inherit</span>
<span class="sd">from.  Throughout pyTenable v1, packages will be transitioning to using this</span>
<span class="sd">base class over the original APISession class.</span>
<span class="sd">.. autoclass:: APIPlatform</span>
<span class="sd">    :members:</span>
<span class="sd">    :inherited-members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">import</span> <span class="nn">os</span>
<span class="kn">import</span> <span class="nn">warnings</span>
<span class="kn">from</span> <span class="nn">restfly</span> <span class="kn">import</span> <span class="n">APISession</span> <span class="k">as</span> <span class="n">Base</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">AuthenticationWarning</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">url_validator</span>
<span class="kn">from</span> <span class="nn">tenable.version</span> <span class="kn">import</span> <span class="n">version</span>
<div class="viewcode-block" id="APIPlatform"><a class="viewcode-back" href="../../../tenable.base.md#tenable.base.platform.APIPlatform">[docs]</a><span class="k">class</span> <span class="nc">APIPlatform</span><span class="p">(</span><span class="n">Base</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Base class for all API Platform packages.  This class handles all of the</span>
<span class="sd">    base connection logic.</span>
<span class="sd">    Args:</span>
<span class="sd">        adaptor (Object, optional):</span>
<span class="sd">            A Requests Session adaptor to bind to the session object.</span>
<span class="sd">        backoff (float, optional):</span>
<span class="sd">            If a 429 response is returned, how much do we want to backoff</span>
<span class="sd">            if the response didn&#39;t send a Retry-After header.  If left</span>
<span class="sd">            unspecified, the default is 1 second.</span>
<span class="sd">        box (bool, optional):</span>
<span class="sd">            Should responses be passed through Box?  If left unspecified, the</span>
<span class="sd">            default is ``True``.</span>
<span class="sd">        box_attrs (dict, optional):</span>
<span class="sd">            Any additional attributes to pass to the Box constructor for this</span>
<span class="sd">            session?  For a list of attributes that can be sent, please refer</span>
<span class="sd">            to the</span>
<span class="sd">            `Box documentation &lt;https://github.com/cdgriffith/Box/wiki&gt;`_</span>
<span class="sd">            for more information.</span>
<span class="sd">        build (str, optional):</span>
<span class="sd">            The build number to put into the User-Agent string.</span>
<span class="sd">        product (str, optional):</span>
<span class="sd">            The product name to put into the User-Agent string.</span>
<span class="sd">        proxies (dict, optional):</span>
<span class="sd">            A dictionary detailing what proxy should be used for what</span>
<span class="sd">            transport protocol.  This value will be passed to the session</span>
<span class="sd">            object after it has been either attached or created.  For</span>
<span class="sd">            details on the structure of this dictionary, consult the</span>
<span class="sd">            :requests:`proxies &lt;user/advanced/#proxies&gt;` section of the</span>
<span class="sd">            Requests documentation.</span>
<span class="sd">        retries (int, optional):</span>
<span class="sd">            The number of retries to make before failing a request.  The</span>
<span class="sd">            default is 5.</span>
<span class="sd">        session (requests.Session, optional):</span>
<span class="sd">            Provide a pre-built session instead of creating a requests</span>
<span class="sd">            session at instantiation.</span>
<span class="sd">        squash_camel (bool, optional):</span>
<span class="sd">            Should the responses have CamelCase responses be squashed into</span>
<span class="sd">            snake_case?  If left unspecified, the default value is ``False``.</span>
<span class="sd">            Note that this will only work when Box is enabled.</span>
<span class="sd">        ssl_verify (bool, optional):</span>
<span class="sd">            If SSL Verification needs to be disabled (for example when using</span>
<span class="sd">            a self-signed certificate), then this parameter should be set to</span>
<span class="sd">            ``False`` to disable verification and mask the Certificate</span>
<span class="sd">            warnings.</span>
<span class="sd">        url (str, optional):</span>
<span class="sd">            The base URL that the paths will be appended onto.</span>
<span class="sd">        vendor (str, optional):</span>
<span class="sd">            The vendor name to put into the User-Agent string.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">_lib_name</span> <span class="o">=</span> <span class="s1">&#39;pyTenable&#39;</span>
    <span class="n">_lib_version</span> <span class="o">=</span> <span class="n">version</span>
    <span class="n">_backoff</span> <span class="o">=</span> <span class="mi">1</span>
    <span class="n">_retries</span> <span class="o">=</span> <span class="mi">5</span>
    <span class="n">_env_base</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span>
    <span class="n">_auth</span> <span class="o">=</span> <span class="p">{}</span>
    <span class="n">_auth_mech</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="c1"># if the constructed URL isn&#39;t valid, then we will throw a TypeError</span>
        <span class="c1"># to inform the caller that something isn&#39;t right here.</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_url</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;url&#39;</span><span class="p">,</span>
                               <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="si">}</span><span class="s1">_URL&#39;</span><span class="p">,</span>
                                              <span class="bp">self</span><span class="o">.</span><span class="n">_url</span>
                                              <span class="p">)</span>
                               <span class="p">)</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">url_validator</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_url</span><span class="p">):</span>
            <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_url</span><span class="si">}</span><span class="s1"> is not a valid URL&#39;</span><span class="p">)</span>
        <span class="c1"># CamelCase squashing is an optional parameter thanks to Box.  if the</span>
        <span class="c1"># user has requested it, then we should add the appropriate parameter</span>
        <span class="c1"># to the box_attrs.</span>
        <span class="k">if</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;squash_camel&#39;</span><span class="p">):</span>
            <span class="n">box_attrs</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;box_attrs&#39;</span><span class="p">,</span> <span class="p">{})</span>
            <span class="n">box_attrs</span><span class="p">[</span><span class="s1">&#39;camel_killer_box&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">bool</span><span class="p">(</span><span class="n">kwargs</span><span class="o">.</span><span class="n">pop</span><span class="p">(</span><span class="s1">&#39;squash_camel&#39;</span><span class="p">))</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;box_attrs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">box_attrs</span>
        <span class="c1"># Call the RESTfly constructor</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">_session_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">password</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Default Session auth behavior</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;session&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;username&#39;</span><span class="p">:</span> <span class="n">username</span><span class="p">,</span>
            <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="n">password</span>
        <span class="p">})</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">=</span> <span class="s1">&#39;user&#39;</span>
    <span class="k">def</span> <span class="nf">_key_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">access_key</span><span class="p">,</span> <span class="n">secret_key</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Default API Key Auth Behavior</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_session</span><span class="o">.</span><span class="n">headers</span><span class="o">.</span><span class="n">update</span><span class="p">({</span>
            <span class="s1">&#39;X-APIKeys&#39;</span><span class="p">:</span> <span class="sa">f</span><span class="s1">&#39;accessKey=</span><span class="si">{</span><span class="n">access_key</span><span class="si">}</span><span class="s1">; secretKey=</span><span class="si">{</span><span class="n">secret_key</span><span class="si">}</span><span class="s1">&#39;</span>
        <span class="p">})</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">=</span> <span class="s1">&#39;keys&#39;</span>
    <span class="k">def</span> <span class="nf">_authenticate</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        This method handles authentication for both API Keys and for session</span>
<span class="sd">        authentication.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># Here we are grafting the authentication functions into the keyword</span>
        <span class="c1"># arguments for later usage.  If a function is provided in the keywords</span>
        <span class="c1"># under the key names below, we will use those instead.  This should</span>
        <span class="c1"># essentially allow for the authentication logic to be overridden with</span>
        <span class="c1"># minimal effort.</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;key_auth_func&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;key_auth_func&#39;</span><span class="p">,</span>
                                             <span class="bp">self</span><span class="o">.</span><span class="n">_key_auth</span><span class="p">)</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;session_auth_func&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;session_auth_func&#39;</span><span class="p">,</span>
                                                 <span class="bp">self</span><span class="o">.</span><span class="n">_session_auth</span><span class="p">)</span>
        <span class="c1"># Pull the API keys from the keyword arguments passed to the</span>
        <span class="c1"># constructor and build the keys tuple.  As API Keys will be</span>
        <span class="c1"># injected directly into the session, there is no need to store these.</span>
        <span class="n">keys</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;_key_auth_dict&#39;</span><span class="p">,</span> <span class="p">{</span>
            <span class="s1">&#39;access_key&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;access_key&#39;</span><span class="p">,</span>
                                     <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="si">}</span><span class="s1">_ACCESS_KEY&#39;</span><span class="p">)</span>
                                     <span class="p">),</span>
            <span class="s1">&#39;secret_key&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;secret_key&#39;</span><span class="p">,</span>
                                     <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="si">}</span><span class="s1">_SECRET_KEY&#39;</span><span class="p">)</span>
                                     <span class="p">)</span>
        <span class="p">})</span>
        <span class="c1"># The session authentication tuple.  We will be storing these as its</span>
        <span class="c1"># possible for the session to timeout on the user.  This would require</span>
        <span class="c1"># re-authentication.</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;_session_auth_dict&#39;</span><span class="p">,</span> <span class="p">{</span>
            <span class="s1">&#39;username&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;username&#39;</span><span class="p">,</span>
                                   <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="si">}</span><span class="s1">_USERNAME&#39;</span><span class="p">)</span>
                                   <span class="p">),</span>
            <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;password&#39;</span><span class="p">,</span>
                                   <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="si">}</span><span class="s1">_PASSWORD&#39;</span><span class="p">)</span>
                                   <span class="p">)</span>
        <span class="p">})</span>
        <span class="c1"># Run the desired authentication function.  As API keys are generally</span>
        <span class="c1"># preferred over session authentication, we will first check to see</span>
        <span class="c1"># that keys have been set, as we prefer stateless auth to stateful.</span>
        <span class="k">if</span> <span class="kc">None</span> <span class="ow">not</span> <span class="ow">in</span> <span class="p">[</span><span class="n">v</span> <span class="k">for</span> <span class="n">_</span><span class="p">,</span> <span class="n">v</span> <span class="ow">in</span> <span class="n">keys</span><span class="o">.</span><span class="n">items</span><span class="p">()]:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;key_auth_func&#39;</span><span class="p">](</span><span class="o">**</span><span class="n">keys</span><span class="p">)</span>
        <span class="k">elif</span> <span class="kc">None</span> <span class="ow">not</span> <span class="ow">in</span> <span class="p">[</span><span class="n">v</span> <span class="k">for</span> <span class="n">_</span><span class="p">,</span> <span class="n">v</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_auth</span><span class="o">.</span><span class="n">items</span><span class="p">()]:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;session_auth_func&#39;</span><span class="p">](</span><span class="o">**</span><span class="bp">self</span><span class="o">.</span><span class="n">_auth</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">warnings</span><span class="o">.</span><span class="n">warn</span><span class="p">(</span><span class="s1">&#39;Starting an unauthenticated session&#39;</span><span class="p">,</span>
                          <span class="n">AuthenticationWarning</span><span class="p">)</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_log</span><span class="o">.</span><span class="n">warning</span><span class="p">(</span><span class="s1">&#39;Starting an unauthenticated session.&#39;</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">_deauthenticate</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>  <span class="c1"># noqa PLW0221</span>
                        <span class="n">method</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="s1">&#39;DELETE&#39;</span><span class="p">,</span>
                        <span class="n">path</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="s1">&#39;session&#39;</span>
                        <span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        This method handles de-authentication.  This is only necessary for</span>
<span class="sd">        session-based authentication.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">==</span> <span class="s1">&#39;user&#39;</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_req</span><span class="p">(</span><span class="n">method</span><span class="p">,</span> <span class="n">path</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth</span> <span class="o">=</span> <span class="p">{}</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">=</span> <span class="kc">None</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.base.platform</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>