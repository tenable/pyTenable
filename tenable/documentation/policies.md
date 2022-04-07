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
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="../sc.md" accesskey="U">tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.policies</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.policies</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Policies</span>
<span class="sd">========</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Scan Policies &lt;Scan-Policy.html&gt;` API.  These items are typically seen</span>
<span class="sd">under the **Scan Policies** section of Tenable.sc.</span>
<span class="sd">Methods available on ``sc.policies``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ScanPolicyAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">UnexpectedValueError</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span><span class="p">,</span> <span class="n">policy_settings</span>
<span class="kn">from</span> <span class="nn">io</span> <span class="kn">import</span> <span class="n">BytesIO</span>
<span class="kn">import</span> <span class="nn">json</span>
<div class="viewcode-block" id="ScanPolicyAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI">[docs]</a><span class="k">class</span> <span class="nc">ScanPolicyAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Document constructor for scan policies.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify that the name attribute is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;context&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify the context if supplied.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;context&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;context&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;scan&#39;</span><span class="p">,</span> <span class="s1">&#39;&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify that the description is a string</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;tags&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify that the tags keyword is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tags&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tags&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;preferences&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that all of the preferences are K:V pairs of strings.</span>
            <span class="k">for</span> <span class="n">key</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;preferences&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">],</span> <span class="nb">dict</span><span class="p">):</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;preference:</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">key</span><span class="p">),</span> <span class="n">key</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;preference:</span><span class="si">{}</span><span class="s1">:value&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">key</span><span class="p">),</span>
                    <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">][</span><span class="n">key</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;audit_files&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># unflatten the audit_files list into a list of dictionaries.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auditFiles&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;auditfile_id&#39;</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">a</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;audit_files&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;audit_files&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;audit_files&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;template_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># convert the policy template id into the appropriate sub-document.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;policyTemplate&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span>
                <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;template_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="p">}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template_id&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;profile_name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># convert the snake-cased &quot;profile_name&quot; into the CamelCase</span>
            <span class="c1"># policyProfileName.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;policyProfileName&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;profile_name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;profile_name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;profile_name&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;xccdf&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># convert the boolean xccdf flag into the string equivalent of</span>
            <span class="c1"># generateXCCDFResults.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;generateXCCDFResults&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;xccdf&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;xccdf&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;xccdf&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;owner_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the owner integer id into CamelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ownerID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;owner_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;owner_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;owner_id&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="ScanPolicyAPI.template_list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.template_list">[docs]</a>    <span class="k">def</span> <span class="nf">template_list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieved the list of scan policy templates.</span>
<span class="sd">        :sc-api:`scan-policy: template-list &lt;Scan-Policy.html#policy_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the policy template list API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of available policy templates</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; templates = sc.policies.template_list()</span>
<span class="sd">            &gt;&gt;&gt; for policy in templates:</span>
<span class="sd">            ...     pprint(policy)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;policyTemplate&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.template_details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.template_details">[docs]</a>    <span class="k">def</span> <span class="nf">template_details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">remove_editor</span><span class="o">=</span><span class="kc">True</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for a specified policy template.</span>
<span class="sd">        :sc-api:`scan-policy: template-details &lt;Scan-Policy-Templates.html#policyTemplate_id_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the policy template</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the policy template details API doc.</span>
<span class="sd">            remove_editor (bol, optional):</span>
<span class="sd">                Should the response have the raw editor string removed?  The</span>
<span class="sd">                default is yes.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                Details about the scan policy template</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; template = sc.policies.template_details(2)</span>
<span class="sd">            &gt;&gt;&gt; pprint(template)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;fields&#39;</span><span class="p">,</span> <span class="n">fields</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;policyTemplate/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;editor&#39;</span> <span class="ow">in</span> <span class="n">resp</span><span class="p">:</span>
            <span class="c1"># Everything is packed JSON, so lets decode the JSON documents into</span>
            <span class="n">editor</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span><span class="n">resp</span><span class="p">[</span><span class="s1">&#39;editor&#39;</span><span class="p">])</span>
            <span class="c1"># Now to decompose the embeddable credentials settings.  What we</span>
            <span class="c1"># intend to do here is return the default settings for every</span>
            <span class="c1"># credential set that can be returned.</span>
            <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;credentials&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
            <span class="k">if</span> <span class="s1">&#39;credentials&#39;</span> <span class="ow">in</span> <span class="n">editor</span><span class="p">:</span>
                <span class="n">emcreds</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span><span class="n">editor</span><span class="p">[</span><span class="s1">&#39;credentials&#39;</span><span class="p">])</span>
                <span class="k">for</span> <span class="n">group</span> <span class="ow">in</span> <span class="n">emcreds</span><span class="p">[</span><span class="s1">&#39;groups&#39;</span><span class="p">]:</span>
                    <span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">group</span><span class="p">[</span><span class="s1">&#39;credentials&#39;</span><span class="p">]:</span>
                        <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;credentials&#39;</span><span class="p">][</span><span class="n">item</span><span class="p">[</span><span class="s1">&#39;id&#39;</span><span class="p">]]</span> <span class="o">=</span> <span class="n">policy_settings</span><span class="p">(</span><span class="n">item</span><span class="p">)</span>
            <span class="c1"># Now to perform the same action as we did for the credentials with</span>
            <span class="c1"># the policy preferences as well.</span>
            <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
            <span class="k">for</span> <span class="n">section</span> <span class="ow">in</span> <span class="n">editor</span><span class="p">[</span><span class="s1">&#39;sections&#39;</span><span class="p">]:</span>
                <span class="k">if</span> <span class="n">section</span><span class="p">[</span><span class="s1">&#39;id&#39;</span><span class="p">]</span> <span class="o">!=</span> <span class="s1">&#39;setup&#39;</span><span class="p">:</span>
                    <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">dict_merge</span><span class="p">(</span><span class="n">resp</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">],</span>
                        <span class="n">policy_settings</span><span class="p">(</span><span class="n">section</span><span class="p">))</span>
            <span class="k">if</span> <span class="n">remove_editor</span><span class="p">:</span>
                <span class="k">del</span><span class="p">(</span><span class="n">resp</span><span class="p">[</span><span class="s1">&#39;editor&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">resp</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieved the list of Scan policies configured.</span>
<span class="sd">        :sc-api:`scan-policy: list &lt;Scan-Policy.html#policy_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the policy list API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                usable &amp; manageable scan policies.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; policies = sc.policies.list()</span>
<span class="sd">            &gt;&gt;&gt; for policy in policies[&#39;manageable&#39;]:</span>
<span class="sd">            ...     pprint(policy)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;fields&#39;</span><span class="p">,</span> <span class="n">fields</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;policy&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for a specified policy.</span>
<span class="sd">        :sc-api:`scan-policy: details &lt;Scan-Policy.html#policy_id_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the policy</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the policy details API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                Details about the scan policy template</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; policy = sc.policies.details(2)</span>
<span class="sd">            &gt;&gt;&gt; pprint(policy)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;fields&#39;</span><span class="p">,</span> <span class="n">fields</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;policy/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new scan policy</span>
<span class="sd">        :sc-api:`scan-policy: create &lt;Scan-Policy.html#policy_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            name (str): The Name of the new scan policy</span>
<span class="sd">            audit_files (list, optional):</span>
<span class="sd">                A list of audit files (by integer id) to be used for the</span>
<span class="sd">                scan policy.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                An optional description for the policy</span>
<span class="sd">            preferences (dict, optional):</span>
<span class="sd">                A dictionary of settings that override the defaults within a</span>
<span class="sd">                policy template.</span>
<span class="sd">            profile_name (str, optional):</span>
<span class="sd">                The profile of the scan.  Default is an empty string.</span>
<span class="sd">            owner_id (int, optional):</span>
<span class="sd">                Define who shall own the policy by that user&#39;s integer identifier</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                An optional tag identifier for the policy</span>
<span class="sd">            template_id (int, optional):</span>
<span class="sd">                The identifier of the policy template to use.  If none is</span>
<span class="sd">                specified, the default id for the &quot;Advanced Policy&quot; will be</span>
<span class="sd">                used.</span>
<span class="sd">            xccdf (bool, optional):</span>
<span class="sd">                Should XCCDF results be generated?  The default is False.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The created scan policy resource.</span>
<span class="sd">        Examples:</span>
<span class="sd">            An example advanced policy with all of the default preferences.</span>
<span class="sd">            &gt;&gt;&gt; sc.policies.create(</span>
<span class="sd">            ...     name=&#39;Example Advanced Policy&#39;)</span>
<span class="sd">            An example policy where we want to modify</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># Firstly we need to check that some specific values are set</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="k">raise</span> <span class="n">UnexpectedValueError</span><span class="p">(</span><span class="s1">&#39;name is a required parameter&#39;</span><span class="p">)</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template_id&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
            <span class="s1">&#39;template_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;template_id&#39;</span><span class="p">,</span> <span class="mi">1</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="c1"># Next we will pull the template details and then pull out the default</span>
        <span class="c1"># settings for the template.</span>
        <span class="n">template</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">template_details</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template_id&#39;</span><span class="p">])</span>
        <span class="c1"># Next, if there are any preferences that the user provided, we will</span>
        <span class="c1"># overlay those on top of the now constructed defaults.</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">dict_merge</span><span class="p">(</span><span class="n">template</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">],</span>
            <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;preferences&#39;</span><span class="p">,</span> <span class="nb">dict</span><span class="p">()))</span>
        <span class="n">policy</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;policy&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">policy</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits an existing scan policy</span>
<span class="sd">        :sc-api:`scan-policy: edit &lt;Scan-Policy.html#policy_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier to the scan policy to edit</span>
<span class="sd">            audit_files (list, optional):</span>
<span class="sd">                A list of audit files (by integer id) to be used for the</span>
<span class="sd">                scan policy.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                An optional description for the policy</span>
<span class="sd">            name (str, optional): The Name of the new scan policy</span>
<span class="sd">            preferences (dict, optional):</span>
<span class="sd">                A dictionary of settings that override the defaults within a</span>
<span class="sd">                policy template.</span>
<span class="sd">            profile_name (str, optional):</span>
<span class="sd">                The profile of the scan.  Default is an empty string.</span>
<span class="sd">            remove_prefs (list, optional):</span>
<span class="sd">                A list of preferences to remove from the policy.</span>
<span class="sd">            owner_id (int, optional):</span>
<span class="sd">                Define who shall own the policy by that user&#39;s integer identifier</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                An optional tag identifier for the policy</span>
<span class="sd">            template_id (int, optional):</span>
<span class="sd">                The identifier of the policy template to use.  If none is</span>
<span class="sd">                specified, the default id for the &quot;Advanced Policy&quot; will be</span>
<span class="sd">                used.</span>
<span class="sd">            xccdf (bool, optional):</span>
<span class="sd">                Should XCCDF results be generated?  The default is False.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The updated scan policy resource.</span>
<span class="sd">        Examples:</span>
<span class="sd">            An example advanced policy with all of the default preferences.</span>
<span class="sd">            &gt;&gt;&gt; sc.policies.edit(10001,</span>
<span class="sd">            ...     name=&#39;Updated Example Advanced Policy&#39;)</span>
<span class="sd">            To remove a preference, you would perform the following:</span>
<span class="sd">            &gt;&gt;&gt; sc.policies.edit(10001,</span>
<span class="sd">            ...     remove_prefs=[&#39;scan_malware&#39;])</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">policy</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="c1"># If remove_prefs is specified, then we will want to validate and move</span>
        <span class="c1"># the values over to the camelCase equiv.</span>
        <span class="k">if</span> <span class="s1">&#39;remove_prefs&#39;</span> <span class="ow">in</span> <span class="n">policy</span><span class="p">:</span>
            <span class="n">policy</span><span class="p">[</span><span class="s1">&#39;removePrefs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;remove:</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">a</span><span class="p">),</span> <span class="n">a</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">a</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;remove_prefs&#39;</span><span class="p">,</span> <span class="n">policy</span><span class="p">[</span><span class="s1">&#39;remove_prefs&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">policy</span><span class="p">[</span><span class="s1">&#39;remove_prefs&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;policy/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">policy</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a configured scan policy.</span>
<span class="sd">        :sc-api:`scan-policy: delete &lt;Scan-Policy.html#policy_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the policy to remove.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                The empty response from the API.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.policies.delete(10001)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;policy/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.copy"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.copy">[docs]</a>    <span class="k">def</span> <span class="nf">copy</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Clones the specified scan policy</span>
<span class="sd">        :sc-api:`scan-policy: copy &lt;Scan-Policy.html#ScanPolicyRESTReference-/policy/{id}/copy&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the source policy to clone.</span>
<span class="sd">            name (str, optional): The name of the new policy.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The scan policy resource record for the newly created policy.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; policy = sc.policies.copy(10001)</span>
<span class="sd">            &gt;&gt;&gt; pprint(policy)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">name</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;policy/</span><span class="si">{}</span><span class="s1">/copy&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.export_policy"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.export_policy">[docs]</a>    <span class="k">def</span> <span class="nf">export_policy</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fobj</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Export the specified scan policy</span>
<span class="sd">        :sc-api:`scan-policy: export &lt;Scan-Policy.html#ScanPolicyRESTReference-/policy/{id}/export&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the scan policy to export.</span>
<span class="sd">            fobj (FileObject, optional):</span>
<span class="sd">                The file-like object to write the resulting file into.  If</span>
<span class="sd">                no file-like object is provided, a BytesIO objects with the</span>
<span class="sd">                downloaded file will be returned.  Be aware that the default</span>
<span class="sd">                option of using a BytesIO object means that the file will be</span>
<span class="sd">                stored in memory, and it&#39;s generally recommended to pass an</span>
<span class="sd">                actual file-object to write to instead.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`FileObject`:</span>
<span class="sd">                The file-like object with the resulting export.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;example_policy.xml&#39;, &#39;wb&#39;) as fobj:</span>
<span class="sd">            ...     sc.policies.export_policy(1001, fobj)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;policy/</span><span class="si">{}</span><span class="s1">/export&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">stream</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="c1"># if no file-like object was passed, then we will instantiate a BytesIO</span>
        <span class="c1"># object to push the file into.</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">fobj</span><span class="p">:</span>
            <span class="n">fobj</span> <span class="o">=</span> <span class="n">BytesIO</span><span class="p">()</span>
        <span class="c1"># Lets stream the file into the file-like object...</span>
        <span class="k">for</span> <span class="n">chunk</span> <span class="ow">in</span> <span class="n">resp</span><span class="o">.</span><span class="n">iter_content</span><span class="p">(</span><span class="n">chunk_size</span><span class="o">=</span><span class="mi">1024</span><span class="p">):</span>
            <span class="k">if</span> <span class="n">chunk</span><span class="p">:</span>
                <span class="n">fobj</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">chunk</span><span class="p">)</span>
        <span class="n">fobj</span><span class="o">.</span><span class="n">seek</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span>
        <span class="n">resp</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
        <span class="k">return</span> <span class="n">fobj</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.import_policy"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.import_policy">[docs]</a>    <span class="k">def</span> <span class="nf">import_policy</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">fobj</span><span class="p">,</span> <span class="n">description</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">tags</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Imports a scan policy into Tenable.sc</span>
<span class="sd">        :sc-api:`scan-policy: import &lt;Scan-Policy.html#ScanPolicyRESTReference-/policy/import&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            name (str): The name of the imported scan policy.</span>
<span class="sd">            fobj (FileObject): The file-like object containing the scan policy.</span>
<span class="sd">            description (str, optional): A description for the scan policy.</span>
<span class="sd">            tags (str, optional): A tag for the scan policy.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response from the API.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;example_policy.xml&#39;, &#39;rb&#39;) as fobj:</span>
<span class="sd">            ...     sc.policies.import_policy(&#39;Example Policy&#39;, fobj)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="nb">str</span><span class="p">)}</span>
        <span class="k">if</span> <span class="n">description</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">description</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">tags</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;tags&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tags&#39;</span><span class="p">,</span> <span class="n">tags</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">fobj</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;policy/import&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.share"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.share">[docs]</a>    <span class="k">def</span> <span class="nf">share</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">groups</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Shares the policy with other user groups.</span>
<span class="sd">        :sc-api:`scan-policy: share &lt;Scan-Policy.html#ScanPolicyRESTReference-/policy/{id}/share&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the scan policy to share.</span>
<span class="sd">            *groups (int): The list of user group ids to share the policy to.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The updated scan policy resource.</span>
<span class="sd">        Examples:</span>
<span class="sd">            Share the scan policy with groups 1, 2, and 3:</span>
<span class="sd">            &gt;&gt;&gt; sc.policies.share(10001, 1, 2, 3)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;policy/</span><span class="si">{}</span><span class="s1">/share&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span><span class="s1">&#39;groups&#39;</span><span class="p">:</span> <span class="p">[{</span>
                <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;group_id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">groups</span><span class="p">]})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScanPolicyAPI.tags"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.policies.ScanPolicyAPI.tags">[docs]</a>    <span class="k">def</span> <span class="nf">tags</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the list of unique tags associated to scan policies.</span>
<span class="sd">        :sc-api:`scan-policy: tags &lt;Scan-Policy.html#ScanPolicyRESTReference-/policy/tag&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                The list of unique tags</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tags = sc.policies.tags()</span>
<span class="sd">            &gt;&gt;&gt; pprint(tags)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;policy/tag&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
          <li class="nav-item nav-item-2"><a href="../sc.md" >tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.policies</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>