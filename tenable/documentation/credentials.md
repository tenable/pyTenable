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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.credentials</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.credentials</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Credentials</span>
<span class="sd">===========</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Scan Credentials &lt;Credential.html&gt;` API.  These</span>
<span class="sd">items are typically seen under the **Scan Credentials** section of Tenable.sc.</span>
<span class="sd">Methods available on ``sc.credentials``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: CredentialAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<div class="viewcode-block" id="CredentialAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI">[docs]</a><span class="k">class</span> <span class="nc">CredentialAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a credential definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">yn</span> <span class="o">=</span> <span class="p">{</span><span class="kc">False</span><span class="p">:</span> <span class="s1">&#39;no&#39;</span><span class="p">,</span> <span class="kc">True</span><span class="p">:</span> <span class="s1">&#39;yes&#39;</span><span class="p">}</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the name parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;tags&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the tags parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tags&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tags&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the description parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the type parameter is a string and falls within the</span>
            <span class="c1"># expected types.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;database&#39;</span><span class="p">,</span> <span class="s1">&#39;windows&#39;</span><span class="p">,</span> <span class="s1">&#39;snmp&#39;</span><span class="p">,</span> <span class="s1">&#39;ssh&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;login&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the login parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;login&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;login&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;sid&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the sid parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;sid&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sid&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;auth_type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the auth_type parameter is a string of the expected</span>
            <span class="c1"># values and then convert it to the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;authType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;auth_type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;cyberark&#39;</span><span class="p">,</span> <span class="s1">&#39;lieberman&#39;</span><span class="p">,</span> <span class="s1">&#39;password&#39;</span><span class="p">,</span> <span class="s1">&#39;BeyondTrust&#39;</span><span class="p">,</span>
                         <span class="s1">&#39;certificate&#39;</span><span class="p">,</span> <span class="s1">&#39;kerberos&#39;</span><span class="p">,</span> <span class="s1">&#39;publicKey&#39;</span><span class="p">,</span> <span class="s1">&#39;thycotic&#39;</span><span class="p">,</span>
                         <span class="s1">&#39;lm&#39;</span><span class="p">,</span> <span class="s1">&#39;ntlm&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;db_type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the db_type parameter is a string of one of the</span>
            <span class="c1"># expected values and then convert it to the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dbType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;db_type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;db_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;Oracle&#39;</span><span class="p">,</span> <span class="s1">&#39;SQL Server&#39;</span><span class="p">,</span> <span class="s1">&#39;DB2&#39;</span><span class="p">,</span> <span class="s1">&#39;MySQL&#39;</span><span class="p">,</span> <span class="s1">&#39;PostgreSQL&#39;</span><span class="p">,</span>
                         <span class="s1">&#39;Informix/DRDA&#39;</span><span class="p">])</span>
            <span class="k">del</span> <span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;db_type&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;port&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the port parameter is a integer and then store the</span>
            <span class="c1"># resulting value as a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;password&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the password parameter is a string type.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;password&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;password&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;username&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the username parameter is a string type.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;username&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;username&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="c1">## CYBERARK AUTH TYPE</span>
        <span class="k">if</span> <span class="s1">&#39;vault_host&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_host parameter is a string type.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_host&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_host&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_port&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_port parameter was passed as an integer</span>
            <span class="c1"># and then store it as a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vault_port&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;vault_username&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that vault_username is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_username&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_username&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_password&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the vault_password is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_password&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_password&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_cyberark_url&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_cyberark_url parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_cyberark_url&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_cyberark_url&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_safe&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_safe parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_safe&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_safe&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_app_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_app_id parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_app_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_app_id&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_policy_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_policy_id parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_policy_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_policy_id&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_folder&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_folder parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_folder&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_folder&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_use_ssl&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_ssl parameter is a boolean value and then</span>
            <span class="c1"># store it as a lowercased string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_use_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vault_use_ssl&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_use_ssl&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
        <span class="k">if</span> <span class="s1">&#39;vault_verify_ssl&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_verify_ssl parameter is a boolean value and</span>
            <span class="c1"># then store is as a lowercased string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_verify_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vault_verify_ssl&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_verify_ssl&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
        <span class="k">if</span> <span class="s1">&#39;vault_address&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the vault_address parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_address&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_address&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_account_name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify that the vault_account_name parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_account_name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_account_name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_cyberark_client_cert&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># verify that the vault_cyberark_client_cert is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_cyberark_client_cert&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_cyberark_client_cert&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_cyberark_private_key&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># verify that the vault_cyberark_private_key param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_cyberark_private_key&#39;</span><span class="p">,</span>
                        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_cyberark_private_key&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;vault_cyberark_private_key_passphrase&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the private key passphrase param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vault_cyberark_private_key_passphrase&#39;</span><span class="p">,</span>
                        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_cyberark_private_key_passphrase&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="c1">### LIEBERMAN AUTH TYPE</span>
        <span class="k">if</span> <span class="s1">&#39;lieberman_host&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the lieberman_host param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lieberman_host&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_host&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;lieberman_port&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the lieberman port param is an integer and then</span>
            <span class="c1"># store it as a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lieberman_port&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;lieberman_pam_user&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the lieberman_pam_user param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lieberman_pam_user&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_pam_user&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;lieberman_pam_password&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the lieberman_pam_password param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lieberman_pam_password&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_pam_password&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;lieberman_use_ssl&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the SSL flag is a boolean value and store it as a</span>
            <span class="c1"># lower-cased string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_use_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lieberman_use_ssl&#39;</span><span class="p">,</span>
                    <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_use_ssl&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
        <span class="k">if</span> <span class="s1">&#39;lieberman_verify_ssl&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the verify SSL flag is a boolean value and store</span>
            <span class="c1"># it as a lower-cased string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_verify_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lieberman_verify_ssl&#39;</span><span class="p">,</span>
                    <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_verify_ssl&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
        <span class="k">if</span> <span class="s1">&#39;lieberman_system_name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the system name is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lieberman_system_name&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_system_name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="c1">### BEYONDTRUST AUTH TYPE</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_host&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the beyondtrust_host param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;beyondtrust_host&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_host&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_port&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the beyondtrust_port is an integer and store it as</span>
            <span class="c1"># a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_port&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_api_key&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the beyondtrust_api_key is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;beyondtrust_api_key&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_api_key&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_duration&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the beyondtrust_duration is an integer value and</span>
            <span class="c1"># store it as a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_duration&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_duration&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_duration&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_use_ssl&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the use_ssl toggle is a boolean value and then store</span>
            <span class="c1"># it as a yes/no string response.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">yn</span><span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_use_ssl&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_ssl&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">)]</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_verify_ssl&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the verify_ssl toggle is a boolean value and then</span>
            <span class="c1"># store it as a yes/no string response.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_verify_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">yn</span><span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_verify_ssl&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_verify_ssl&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">)]</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_use_private_key&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the use_private_key toggle is a boolean value and</span>
            <span class="c1"># then store it as a yes/no string response.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_private_key&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">yn</span><span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_use_private_key&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_private_key&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">)]</span>
        <span class="k">if</span> <span class="s1">&#39;beyondtrust_use_escalation&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the use_escalation toggle is a boolean value and</span>
            <span class="c1"># then store it as a yes/no string response.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_escalation&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">yn</span><span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_use_escalation&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_escalation&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">)]</span>
        <span class="c1">### AUTHTYPE THYCOTIC</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_secret_name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the secret name param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_secret_name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_secret_name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_url&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the url is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_url&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_url&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_username&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the username is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_username&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_username&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_password&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the password is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_password&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_password&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_organization&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the organization is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_organization&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_organization&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_domain&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the domain is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_domain&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_domain&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_private_key&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the private key flag is a boolean value and then</span>
            <span class="c1"># store it as a yes/no string equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_private_key&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">yn</span><span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_private_key&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_private_key&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">)]</span>
        <span class="k">if</span> <span class="s1">&#39;thycotic_ssl_verify&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the ssl verification flag is a boolean value and</span>
            <span class="c1"># then store it as a yes/no string equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_ssl_verify&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">yn</span><span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;thycotic_ssl_verify&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_ssl_verify&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">)]</span>
        <span class="c1">### AUTHTYPE CERTIFICATE</span>
        <span class="k">if</span> <span class="s1">&#39;public_key&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the public_key param is a string and then store in</span>
            <span class="c1"># the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;publicKey&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;public_key&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;public_key&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;public_key&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;private_key&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the private_key param is a string and then store it</span>
            <span class="c1"># in the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;privateKey&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;private_key&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;private_key&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;private_key&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;passphrase&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the passphrase param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;passphrase&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;passphrase&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;privilege_escalation&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that privilege_escalation is a string value of one of the</span>
            <span class="c1"># expected types and store it in the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;privilegeEscalation&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;privilege_escalation&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;privilege_escalation&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                    <span class="s1">&#39;none&#39;</span><span class="p">,</span> <span class="s1">&#39;su&#39;</span><span class="p">,</span> <span class="s1">&#39;sudo&#39;</span><span class="p">,</span> <span class="s1">&#39;su+sudo&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;dzdo&#39;</span><span class="p">,</span> <span class="s1">&#39;pbrun&#39;</span><span class="p">,</span> <span class="s1">&#39;cisco&#39;</span><span class="p">,</span> <span class="s1">&#39;.k5login&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;privilege_escalation&#39;</span><span class="p">])</span>
        <span class="c1">### KERBEROS AUTHTYPE</span>
        <span class="k">if</span> <span class="s1">&#39;kdc_ip&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the ip value is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;kdc_ip&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_ip&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;kdc_port&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the port value is an integer and store it as a str.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;kdc_port&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;kdc_protocol&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the protocol value is a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_protocol&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;kdc_protocol&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_protocol&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;UDP&#39;</span><span class="p">,</span> <span class="s1">&#39;TCP&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;kdc_realm&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the realm value is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;kdc_realm&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_realm&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="c1">### ORACLE DB TYPE</span>
        <span class="k">if</span> <span class="s1">&#39;oracle_auth_type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the oracle_auth_type var is a string and then store</span>
            <span class="c1"># it in the camelCased equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;oracleAuthType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;oracle_auth_type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;oracle_auth_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;SYSDBA&#39;</span><span class="p">,</span> <span class="s1">&#39;SYSOPER&#39;</span><span class="p">,</span> <span class="s1">&#39;NORMAL&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;oracle_auth_type&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;oracle_service_type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the oracle_service_type var is a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;oracle_service_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;oracle_service_type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;oracle_service_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;SID&#39;</span><span class="p">,</span> <span class="s1">&#39;SERVICE_NAME&#39;</span><span class="p">])</span>
        <span class="c1">### SQL SERVER DB TYPE</span>
        <span class="k">if</span> <span class="s1">&#39;sql_server_auth_type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the sql_server_auth_type var is a string and store</span>
            <span class="c1"># it in the camelCased variant expected,</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;SQLServerAuthType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;sql_server_auth_type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sql_server_auth_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;SQL&#39;</span><span class="p">,</span> <span class="s1">&#39;Windows&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sql_server_auth_type&#39;</span><span class="p">])</span>
        <span class="c1">### PRIV ESCALATION PARAMS</span>
        <span class="k">if</span> <span class="s1">&#39;escalation_username&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify that the escalation username is a string and store it in</span>
            <span class="c1"># the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalationUsername&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;escalation_username&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_username&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_username&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;escalation_password&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the escalation password is a string and store it in</span>
            <span class="c1"># the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalationPassword&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;escalation_password&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_password&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_password&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;escalation_path&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the escalation path is a string and store it in the</span>
            <span class="c1"># camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalationPath&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;escalation_path&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_path&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_path&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;escalation_su_user&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the escalation SU user is a string and store it in</span>
            <span class="c1"># the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalationSuUser&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;escalation_su_user&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_su_user&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;escalation_su_user&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;community_string&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the community string is a string value and store it</span>
            <span class="c1"># in the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;communityString&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;community_string&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;community_string&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;community_string&#39;</span><span class="p">])</span>
        <span class="c1">### WINDOWS AUTH TYPE STUFF</span>
        <span class="k">if</span> <span class="s1">&#39;domain&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the domain param is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;domain&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;domain&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">kw</span>
    <span class="k">def</span> <span class="nf">_upload_files</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Uploads the file objects specified and returns the filename attributes</span>
<span class="sd">        associated to each keyword.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">uploadable_keys</span> <span class="o">=</span> <span class="p">[</span>
            <span class="s1">&#39;vault_cyberark_client_cert&#39;</span><span class="p">,</span> <span class="s1">&#39;vault_cyberark_private_key&#39;</span><span class="p">,</span>
            <span class="s1">&#39;public_key&#39;</span><span class="p">,</span> <span class="s1">&#39;private_key&#39;</span><span class="p">,</span>
        <span class="p">]</span>
        <span class="k">for</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">uploadable_keys</span><span class="p">:</span>
            <span class="k">if</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="n">key</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="n">key</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="CredentialAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">cred_type</span><span class="p">,</span> <span class="n">auth_type</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a credential.</span>
<span class="sd">        :sc-api:`credential: create &lt;Credential.html#credential_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            name (str): The name for the credential.</span>
<span class="sd">            cred_type (str):</span>
<span class="sd">                The type of credential to store.  Valid types are ``database``,</span>
<span class="sd">                ``snmp``, ``ssh``, and ``windows``.</span>
<span class="sd">            auth_type (str):</span>
<span class="sd">                The type of authentication for the credential.  Valid types are</span>
<span class="sd">                ``beyondtrust``, ``certificate``, cyberark``, ``kerberos``,</span>
<span class="sd">                ``lieberman``, ``lm``, ``ntlm``, ``password``, ``publicKey``,</span>
<span class="sd">                ``thycotic``.</span>
<span class="sd">            beyondtrust_api_key (str, optional):</span>
<span class="sd">                The API key to use for authenticating to Beyondtrust.</span>
<span class="sd">            beyondtrust_duration (int, optional):</span>
<span class="sd">                The length of time to cache the checked-out credentials from</span>
<span class="sd">                Beyondtrust.  This value should be less than the password change</span>
<span class="sd">                interval within Beyondtrust.</span>
<span class="sd">            beyondtrust_host (str, optional):</span>
<span class="sd">                The host address for the Beyondtrust application.</span>
<span class="sd">            beyondtrust_port (int, optional):</span>
<span class="sd">                The port number associated with the Beyondtrust application.</span>
<span class="sd">            beyondtrust_use_escalation (bool, optional):</span>
<span class="sd">                If enabled, informs the scanners to use Beyondtrust for</span>
<span class="sd">                privilege escalation.</span>
<span class="sd">            beyondtrust_use_private_key (bool, optional):</span>
<span class="sd">                If enabled, informs the scanners to use key-based auth for SSH</span>
<span class="sd">                connections instead of password auth.</span>
<span class="sd">            beyondtrust_use_ssl (bool, optional):</span>
<span class="sd">                Should the scanners communicate to Beyondtrust over SSL for</span>
<span class="sd">                credential retrieval?  If left unspecified, the default is set</span>
<span class="sd">                to ``True``.</span>
<span class="sd">            beyondtrust_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                Beyondtrust?  If left unspecified, the default is ``False``.</span>
<span class="sd">            community_string (str, optional):</span>
<span class="sd">                The SNMP community string to use for authentication.</span>
<span class="sd">            db_type (str, optional):</span>
<span class="sd">                The type of database connection that will be performed.  Valid</span>
<span class="sd">                types are ``DB2``, ``Informix/DRDA``, ``MySQL``, ``Oracle``,</span>
<span class="sd">                ``PostgreSQL``, ``SQL Server``.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                A description to associate to the credential.</span>
<span class="sd">            domain (str, optional):</span>
<span class="sd">                The Active Directory domain to use if the user is a member of a</span>
<span class="sd">                domain.</span>
<span class="sd">            escalation_path (str, optional):</span>
<span class="sd">                The path in which to run the escalation commands.</span>
<span class="sd">            escalation_password (str, optional):</span>
<span class="sd">                The password to use for the escalation.</span>
<span class="sd">            escalation_su_use (str, optional):</span>
<span class="sd">                If performing an SU escalation, this is the user to escalate to.</span>
<span class="sd">            escalation_username (str, optional):</span>
<span class="sd">                The username to escalate to.</span>
<span class="sd">            kdc_ip (str, optional):</span>
<span class="sd">                The kerberos host supplying the session tickets.</span>
<span class="sd">            kdc_port (int, optional):</span>
<span class="sd">                The port to use for kerberos connections.  If left unspecified</span>
<span class="sd">                the default is ``88``.</span>
<span class="sd">            kdc_protocol (str, optional):</span>
<span class="sd">                The protocol to use for kerberos connections.  Valid options are</span>
<span class="sd">                ``tcp`` and ``udp``.  If left unspecified then the default is</span>
<span class="sd">                ``tcp``.</span>
<span class="sd">            kdc_realm (str, optional):</span>
<span class="sd">                The Kerberos realm to use for authentication.</span>
<span class="sd">            lieberman_host (str, optional):</span>
<span class="sd">                The address for the Lieberman vault.</span>
<span class="sd">            lieberman_port (int, optional):</span>
<span class="sd">                The port number where the Lieberman service is listening.</span>
<span class="sd">            lieberman_pam_password (str, optional):</span>
<span class="sd">                The password to authenticate to the Lieberman RED API.</span>
<span class="sd">            lieberman_pam_user (str, optional):</span>
<span class="sd">                The username to authenticate to the Lieberman RED API.</span>
<span class="sd">            lieberman_system_name (str, optional):</span>
<span class="sd">                The name for the credentials in Lieberman.</span>
<span class="sd">            lieberman_use_ssl (bool, optional):</span>
<span class="sd">                Should the scanners communicate to Lieberman over SSL for</span>
<span class="sd">                credential retrieval?  If left unspecified, the default is set</span>
<span class="sd">                to ``True``.</span>
<span class="sd">            lieberman_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                Lieberman?  If left unspecified, the default is ``False``.</span>
<span class="sd">            password (str, optional):</span>
<span class="sd">                The password for the credential.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                A valid port number for a database credential.</span>
<span class="sd">            private_key (file, optional):</span>
<span class="sd">                The fileobject containing the SSH private key.</span>
<span class="sd">            privilege_escalation (str, optional):</span>
<span class="sd">                The type of privilege escalation to perform once authenticated.</span>
<span class="sd">                Valid values are ``.k5login``, ``cisco``, ``dzdo``, ``none``,</span>
<span class="sd">                ``pbrun``, ``su``, ``su+sudo``, ``sudo``.  If left unspecified,</span>
<span class="sd">                the default is ``none``.</span>
<span class="sd">            public_key (file, optional):</span>
<span class="sd">                The fileobject containing the SSH public key or certificate.</span>
<span class="sd">            oracle_auth_type (str, optional):</span>
<span class="sd">                The type of authentication to use when communicating to an</span>
<span class="sd">                Oracle database server.  Supported values are ``sysdba``,</span>
<span class="sd">                ``sysoper``, and ``normal``.  If left unspecified, the default</span>
<span class="sd">                option is ``normal``.</span>
<span class="sd">            oracle_service_type (str, optional):</span>
<span class="sd">                The type of service identifier specified in the ``sid``</span>
<span class="sd">                parameter.  Valid values are either ``sid`` or ``service_name``.</span>
<span class="sd">                If left unspecified, the default is ``sid``.</span>
<span class="sd">            sid (str, optional):</span>
<span class="sd">                The service identifier or name for a database credential.</span>
<span class="sd">            sql_server_auth_type (str, optional):</span>
<span class="sd">                The type of authentication to perform to the SQL Server</span>
<span class="sd">                instance.  Valid values are ``SQL`` and ``Windows``.  The default</span>
<span class="sd">                value if left unspecified is ``SQL``.</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                A tag to associate to the credential.</span>
<span class="sd">            username (str, optional):</span>
<span class="sd">                The username for the OS credential.</span>
<span class="sd">            thycotic_domain (str, optional):</span>
<span class="sd">                The domain, if set, within Thycotic.</span>
<span class="sd">            thycotic_organization (str, optional):</span>
<span class="sd">                The organization to use if using a cloud instance of Thycotic.</span>
<span class="sd">            thycotic_password (str, optional):</span>
<span class="sd">                The password to use when authenticating to Thycotic.</span>
<span class="sd">            thycotic_private_key (bool, optional):</span>
<span class="sd">                If enabled, informs the scanners to use key-based auth for SSH</span>
<span class="sd">                connections instead of password auth.</span>
<span class="sd">            thycotic_secret_name (str, optional):</span>
<span class="sd">                The secret name value on the Tycotic server.</span>
<span class="sd">            thycotic_url (str, optional):</span>
<span class="sd">                The absolute URL path pointing to the Thycotic secret server.</span>
<span class="sd">            thycotic_username (str, optional):</span>
<span class="sd">                The username to use to authenticate to Thycotic.</span>
<span class="sd">            thycotic_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                Thycotic?  If left unspecified, the default is ``False``.</span>
<span class="sd">            vault_account_name (str, optional):</span>
<span class="sd">                The unique name of the credential to retrieve from CyberArk.</span>
<span class="sd">                Generally referred to as the *name* parameter within CyberArk.</span>
<span class="sd">            vault_address (str, optional):</span>
<span class="sd">                The domain for the CyberArk account.  SSL must be configured</span>
<span class="sd">                through IIS on the CCP before using.</span>
<span class="sd">            vault_app_id (str, optional):</span>
<span class="sd">                The AppID to use with CyberArk.</span>
<span class="sd">            vault_cyberark_client_cert (file, optional):</span>
<span class="sd">                The fileobject containing the CyberArk client certificate.</span>
<span class="sd">            vault_cyberark_url (str, optional):</span>
<span class="sd">                The URL for the CyberArk AIM web service. If left unspecified,</span>
<span class="sd">                the default URL path of ``/AIMWebservice/v1.1/AIM.asmx`` will be</span>
<span class="sd">                used..</span>
<span class="sd">            vault_cyberark_private_key (file, optional):</span>
<span class="sd">                The fileobject containing the CyberArk client private key.</span>
<span class="sd">            vault_cyberark_private_key_passphrase (str, optional):</span>
<span class="sd">                The passhrase for the private key.</span>
<span class="sd">            vault_folder (str, optional):</span>
<span class="sd">                The folder to use within CyberArk for credential retrieval.</span>
<span class="sd">            vault_host (str, optional):</span>
<span class="sd">                The CyberArk Vault host.</span>
<span class="sd">            vault_password (str, optional):</span>
<span class="sd">                The password to use for authentication to the vault if</span>
<span class="sd">                the CyberArk Central Credential Provider is configured for</span>
<span class="sd">                basic auth.</span>
<span class="sd">            vault_policy_id (int, optional):</span>
<span class="sd">                The CyberArk PolicyID assigned to the credentials to retrieve.</span>
<span class="sd">            vault_port (int, optional):</span>
<span class="sd">                The port in which the CyberArk Vault resides.</span>
<span class="sd">            vault_safe (str, optional):</span>
<span class="sd">                The CyberArk safe that contains the credentials to retrieve.</span>
<span class="sd">            vault_use_ssl (bool, optional):</span>
<span class="sd">                Should the scanners communicate to CyberArk over SSL for</span>
<span class="sd">                credential retrieval?  If left unspecified, the default is set</span>
<span class="sd">                to ``True``.</span>
<span class="sd">            vault_username (str, optional):</span>
<span class="sd">                The username to use for authentication to the vault if</span>
<span class="sd">                the CyberArk Central Credential Provider is configured for</span>
<span class="sd">                basic auth.</span>
<span class="sd">            vault_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                the vault?  If left unspecified, the default is ``False``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created credential.</span>
<span class="sd">        Examples:</span>
<span class="sd">            Creating a Windows AD credential:</span>
<span class="sd">            &gt;&gt;&gt; cred = sc.credentials.create(</span>
<span class="sd">            ...     &#39;Example AD User&#39;, &#39;windows&#39;, &#39;ntlm&#39;,</span>
<span class="sd">            ...     username=&#39;scanneruser&#39;,</span>
<span class="sd">            ...     password=&#39;sekretpassword&#39;,</span>
<span class="sd">            ...     domain=&#39;Company.com&#39;)</span>
<span class="sd">            Creating a root user SSH credential:</span>
<span class="sd">            &gt;&gt;&gt; cred = sc.credentials.create(</span>
<span class="sd">            ...     &#39;Example SSH Cred&#39;, &#39;ssh&#39;, &#39;password&#39;,</span>
<span class="sd">            ...     username=&#39;root&#39;,</span>
<span class="sd">            ...     password=&#39;sekretpassword&#39;)</span>
<span class="sd">            Creating a root user SSH cred with a private key:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;privatekeyfile&#39;, &#39;rb&#39;) as keyfile:</span>
<span class="sd">            ...     cred = sc.credentials.create(</span>
<span class="sd">            ...         &#39;Example SSH Keys&#39;, &#39;ssh&#39;, &#39;publickey&#39;,</span>
<span class="sd">            ...         username=&#39;root&#39;,</span>
<span class="sd">            ...         private_key=keyfile)</span>
<span class="sd">            Creating a normal user SSH cred with sudo for privilege escalation:</span>
<span class="sd">            &gt;&gt;&gt; cred = sc.credentials.create(</span>
<span class="sd">            ...     &#39;Example SSH Sudo&#39;, &#39;ssh&#39;, &#39;password&#39;,</span>
<span class="sd">            ...     username=&#39;user&#39;,</span>
<span class="sd">            ...     password=&#39;sekretpassword&#39;,</span>
<span class="sd">            ...     privilege_escalation=&#39;sudo&#39;,</span>
<span class="sd">            ...     escalation_password=&#39;sekretpassword&#39;)</span>
<span class="sd">            Creating a SQL Server cred set:</span>
<span class="sd">            &gt;&gt;&gt; cred = sc.credentials.create(</span>
<span class="sd">            ...     &#39;Example SQL Server&#39;, &#39;database&#39;, &#39;SQL Server&#39;,</span>
<span class="sd">            ...     username=&#39;sa&#39;,</span>
<span class="sd">            ...     password=&#39;sekretpassword&#39;,</span>
<span class="sd">            ...     sql_server_auth_type=&#39;SQL&#39;,</span>
<span class="sd">            ...     sid=&#39;database_name&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">cred_type</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">auth_type</span>
        <span class="c1"># Setting some default values depending on what&#39;s passed.  Generally</span>
        <span class="c1"># speaking we want to default to using SSL, however by default not</span>
        <span class="c1"># verify the SSL certificate (as generally these are on-prem systems</span>
        <span class="c1"># with a self-signed cert)</span>
        <span class="k">if</span> <span class="n">auth_type</span> <span class="o">==</span> <span class="s1">&#39;cyberark&#39;</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_use_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;vault_use_ssl&#39;</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vault_verify_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;vault_verify_ssl&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
        <span class="k">elif</span> <span class="n">auth_type</span> <span class="o">==</span> <span class="s1">&#39;lieberman&#39;</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_use_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;lieberman_use_ssl&#39;</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lieberman_verify_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;lieberman_verify_ssl&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
        <span class="k">elif</span> <span class="n">auth_type</span> <span class="o">==</span> <span class="s1">&#39;beyondtrust&#39;</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;BeyondTrust&#39;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;beyondtrust_use_ssl&#39;</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_verify_ssl&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_verify_ssl&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_private_key&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_use_private_key&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;beyondtrust_use_escalation&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
                <span class="s1">&#39;beyondtrust_use_escalation&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
        <span class="k">elif</span> <span class="n">auth_type</span> <span class="o">==</span> <span class="s1">&#39;thycotic&#39;</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_ssl_verify&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;thycotic_ssl_verify&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
            <span class="k">if</span> <span class="n">cred_type</span> <span class="o">==</span> <span class="s1">&#39;ssh&#39;</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;thycotic_private_key&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
                    <span class="s1">&#39;thycotic_private_key&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
        <span class="k">elif</span> <span class="n">auth_type</span> <span class="o">==</span> <span class="s1">&#39;kerberos&#39;</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;kdc_port&#39;</span><span class="p">,</span> <span class="mi">88</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;kdc_protocol&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;kdc_protocol&#39;</span><span class="p">,</span> <span class="s1">&#39;tcp&#39;</span><span class="p">)</span>
        <span class="c1"># If the credential type is ssh, then we&#39;d like to make sure that</span>
        <span class="c1"># the escalation is set to &quot;none&quot; unless overridden.</span>
        <span class="k">if</span> <span class="p">(</span><span class="n">cred_type</span> <span class="o">==</span> <span class="s1">&#39;ssh&#39;</span>
          <span class="ow">and</span> <span class="n">auth_type</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;password&#39;</span><span class="p">,</span> <span class="s1">&#39;publicKey&#39;</span><span class="p">,</span> <span class="s1">&#39;certificate&#39;</span><span class="p">]):</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;privilege_escalation&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;privilege_escalation&#39;</span><span class="p">,</span> <span class="s1">&#39;none&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;db_type&#39;</span><span class="p">)</span> <span class="o">==</span> <span class="s1">&#39;Oracle&#39;</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;oracle_auth_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;oracle_auth_type&#39;</span><span class="p">,</span> <span class="s1">&#39;NORMAL&#39;</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;oracle_service_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;oracle_service_type&#39;</span><span class="p">,</span> <span class="s1">&#39;SID&#39;</span><span class="p">)</span>
        <span class="c1"># Uploading files as necessary</span>
        <span class="n">kw</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_upload_files</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="c1"># Constructing the payload</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="c1"># Making the call.</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;credential&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CredentialAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific credential.</span>
<span class="sd">        :sc-api:`credential: details &lt;Credential.html#CredentialRESTReference-/credential/{id}&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the credential.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The credential resource record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; cred = sc.credentials.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(cred)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;credential/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CredentialAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits a credential.</span>
<span class="sd">        :sc-api:`credential: edit &lt;Credential.html#credential_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            auth_type (str, optional):</span>
<span class="sd">                The type of authentication for the credential.  Valid types are</span>
<span class="sd">                ``beyondtrust``, ``certificate``, cyberark``, ``kerberos``,</span>
<span class="sd">                ``lieberman``, ``lm``, ``ntlm``, ``password``, ``publickey``,</span>
<span class="sd">                ``thycotic``.</span>
<span class="sd">            beyondtrust_api_key (str, optional):</span>
<span class="sd">                The API key to use for authenticating to Beyondtrust.</span>
<span class="sd">            beyondtrust_duration (int, optional):</span>
<span class="sd">                The length of time to cache the checked-out credentials from</span>
<span class="sd">                Beyondtrust.  This value should be less than the password change</span>
<span class="sd">                interval within Beyondtrust.</span>
<span class="sd">            beyondtrust_host (str, optional):</span>
<span class="sd">                The host address for the Beyondtrust application.</span>
<span class="sd">            beyondtrust_port (int, optional):</span>
<span class="sd">                The port number associated with the Beyondtrust application.</span>
<span class="sd">            beyondtrust_use_escalation (bool, optional):</span>
<span class="sd">                If enabled, informs the scanners to use Beyondtrust for</span>
<span class="sd">                privilege escalation.</span>
<span class="sd">            beyondtrust_use_private_key (bool, optional):</span>
<span class="sd">                If enabled, informs the scanners to use key-based auth for SSH</span>
<span class="sd">                connections instead of password auth.</span>
<span class="sd">            beyondtrust_use_ssl (bool, optional):</span>
<span class="sd">                Should the scanners communicate to Beyondtrust over SSL for</span>
<span class="sd">                credential retrieval?  If left unspecified, the default is set</span>
<span class="sd">                to ``True``.</span>
<span class="sd">            beyondtrust_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                Beyondtrust?  If left unspecified, the default is ``False``.</span>
<span class="sd">            community_string (str, optional):</span>
<span class="sd">                The SNMP community string to use for authentication.</span>
<span class="sd">            db_type (str, optional):</span>
<span class="sd">                The type of database connection that will be performed.  Valid</span>
<span class="sd">                types are ``DB2``, ``Informix/DRDA``, ``MySQL``, ``Oracle``,</span>
<span class="sd">                ``PostgreSQL``, ``SQL Server``.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                A description to associate to the credential.</span>
<span class="sd">            domain (str, optional):</span>
<span class="sd">                The Active Directory domain to use if the user is a member of a</span>
<span class="sd">                domain.</span>
<span class="sd">            escalation_path (str, optional):</span>
<span class="sd">                The path in which to run the escalation commands.</span>
<span class="sd">            escalation_password (str, optional):</span>
<span class="sd">                The password to use for the escalation.</span>
<span class="sd">            escalation_su_use (str, optional):</span>
<span class="sd">                If performing an SU escalation, this is the user to escalate to.</span>
<span class="sd">            escalation_username (str, optional):</span>
<span class="sd">                The username to escalate to.</span>
<span class="sd">            kdc_ip (str, optional):</span>
<span class="sd">                The kerberos host supplying the session tickets.</span>
<span class="sd">            kdc_port (int, optional):</span>
<span class="sd">                The port to use for kerberos connections.  If left unspecified</span>
<span class="sd">                the default is ``88``.</span>
<span class="sd">            kdc_protocol (str, optional):</span>
<span class="sd">                The protocol to use for kerberos connections.  Valid options are</span>
<span class="sd">                ``tcp`` and ``udp``.  If left unspecified then the default is</span>
<span class="sd">                ``tcp``.</span>
<span class="sd">            kdc_realm (str, optional):</span>
<span class="sd">                The Kerberos realm to use for authentication.</span>
<span class="sd">            lieberman_host (str, optional):</span>
<span class="sd">                The address for the Lieberman vault.</span>
<span class="sd">            lieberman_port (int, optional):</span>
<span class="sd">                The port number where the Lieberman service is listening.</span>
<span class="sd">            lieberman_pam_password (str, optional):</span>
<span class="sd">                The password to authenticate to the Lieberman RED API.</span>
<span class="sd">            lieberman_pam_user (str, optional):</span>
<span class="sd">                The username to authenticate to the Lieberman RED API.</span>
<span class="sd">            lieberman_system_name (str, optional):</span>
<span class="sd">                The name for the credentials in Lieberman.</span>
<span class="sd">            lieberman_use_ssl (bool, optional):</span>
<span class="sd">                Should the scanners communicate to Lieberman over SSL for</span>
<span class="sd">                credential retrieval?  If left unspecified, the default is set</span>
<span class="sd">                to ``True``.</span>
<span class="sd">            lieberman_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                Lieberman?  If left unspecified, the default is ``False``.</span>
<span class="sd">            name (str, optional):</span>
<span class="sd">                The name for the credential.</span>
<span class="sd">            password (str, optional):</span>
<span class="sd">                The password for the credential.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                A valid port number for a database credential.</span>
<span class="sd">            private_key (file, optional):</span>
<span class="sd">                The fileobject containing the SSH private key.</span>
<span class="sd">            privilege_escalation (str, optional):</span>
<span class="sd">                The type of privilege escalation to perform once authenticated.</span>
<span class="sd">                Valid values are ``.k5login``, ``cisco``, ``dzdo``, ``none``,</span>
<span class="sd">                ``pbrun``, ``su``, ``su+sudo``, ``sudo``.  If left unspecified,</span>
<span class="sd">                the default is ``none``.</span>
<span class="sd">            public_key (file, optional):</span>
<span class="sd">                The fileobject containing the SSH public key or certificate.</span>
<span class="sd">            oracle_auth_type (str, optional):</span>
<span class="sd">                The type of authentication to use when communicating to an</span>
<span class="sd">                Oracle database server.  Supported values are ``sysdba``,</span>
<span class="sd">                ``sysoper``, and ``normal``.  If left unspecified, the default</span>
<span class="sd">                option is ``normal``.</span>
<span class="sd">            oracle_service_type (str, optional):</span>
<span class="sd">                The type of service identifier specified in the ``sid``</span>
<span class="sd">                parameter.  Valid values are either ``sid`` or ``service_name``.</span>
<span class="sd">                If left unspecified, the default is ``sid``.</span>
<span class="sd">            sid (str, optional):</span>
<span class="sd">                The service identifier or name for a database credential.</span>
<span class="sd">            sql_server_auth_type (str, optional):</span>
<span class="sd">                The type of authentication to perform to the SQL Server</span>
<span class="sd">                instance.  Valid values are ``SQL`` and ``Windows``.  The default</span>
<span class="sd">                value if left unspecified is ``SQL``.</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                A tag to associate to the credential.</span>
<span class="sd">            type (str. optional):</span>
<span class="sd">                The type of credential to store.  Valid types are ``database``,</span>
<span class="sd">                ``snmp``, ``ssh``, and ``windows``.</span>
<span class="sd">            username (str, optional):</span>
<span class="sd">                The username for the OS credential.</span>
<span class="sd">            thycotic_domain (str, optional):</span>
<span class="sd">                The domain, if set, within Thycotic.</span>
<span class="sd">            thycotic_organization (str, optional):</span>
<span class="sd">                The organization to use if using a cloud instance of Thycotic.</span>
<span class="sd">            thycotic_password (str, optional):</span>
<span class="sd">                The password to use when authenticating to Thycotic.</span>
<span class="sd">            thycotic_private_key (bool, optional):</span>
<span class="sd">                If enabled, informs the scanners to use key-based auth for SSH</span>
<span class="sd">                connections instead of password auth.</span>
<span class="sd">            thycotic_secret_name (str, optional):</span>
<span class="sd">                The secret name value on the Tycotic server.</span>
<span class="sd">            thycotic_url (str, optional):</span>
<span class="sd">                The absolute URL path pointing to the Thycotic secret server.</span>
<span class="sd">            thycotic_username (str, optional):</span>
<span class="sd">                The username to use to authenticate to Thycotic.</span>
<span class="sd">            thycotic_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                Thycotic?  If left unspecified, the default is ``False``.</span>
<span class="sd">            vault_account_name (str, optional):</span>
<span class="sd">                The unique name of the credential to retrieve from CyberArk.</span>
<span class="sd">                Generally referred to as the *name* parameter within CyberArk.</span>
<span class="sd">            vault_address (str, optional):</span>
<span class="sd">                The domain for the CyberArk account.  SSL must be configured</span>
<span class="sd">                through IIS on the CCP before using.</span>
<span class="sd">            vault_app_id (str, optional):</span>
<span class="sd">                The AppID to use with CyberArk.</span>
<span class="sd">            vault_cyberark_client_cert (file, optional):</span>
<span class="sd">                The fileobject containing the CyberArk client certificate.</span>
<span class="sd">            vault_cyberark_url (str, optional):</span>
<span class="sd">                The URL for the CyberArk AIM web service. If left unspecified,</span>
<span class="sd">                the default URL path of ``/AIMWebservice/v1.1/AIM.asmx`` will be</span>
<span class="sd">                used..</span>
<span class="sd">            vault_cyberark_private_key (file, optional):</span>
<span class="sd">                The fileobject containing the CyberArk client private key.</span>
<span class="sd">            vault_cyberark_private_key_passphrase (str, optional):</span>
<span class="sd">                The passhrase for the private key.</span>
<span class="sd">            vault_folder (str, optional):</span>
<span class="sd">                The folder to use within CyberArk for credential retrieval.</span>
<span class="sd">            vault_host (str, optional):</span>
<span class="sd">                The CyberArk Vault host.</span>
<span class="sd">            vault_password (str, optional):</span>
<span class="sd">                The password to use for authentication to the vault if</span>
<span class="sd">                the CyberArk Central Credential Provider is configured for</span>
<span class="sd">                basic auth.</span>
<span class="sd">            vault_policy_id (int, optional):</span>
<span class="sd">                The CyberArk PolicyID assigned to the credentials to retrieve.</span>
<span class="sd">            vault_port (int, optional):</span>
<span class="sd">                The port in which the CyberArk Vault resides.</span>
<span class="sd">            vault_safe (str, optional):</span>
<span class="sd">                The CyberArk safe that contains the credentials to retrieve.</span>
<span class="sd">            vault_use_ssl (bool, optional):</span>
<span class="sd">                Should the scanners communicate to CyberArk over SSL for</span>
<span class="sd">                credential retrieval?  If left unspecified, the default is set</span>
<span class="sd">                to ``True``.</span>
<span class="sd">            vault_username (str, optional):</span>
<span class="sd">                The username to use for authentication to the vault if</span>
<span class="sd">                the CyberArk Central Credential Provider is configured for</span>
<span class="sd">                basic auth.</span>
<span class="sd">            vault_verify_ssl (bool, optional):</span>
<span class="sd">                Should the SSL certificate be validated when communicating to</span>
<span class="sd">                the vault?  If left unspecified, the default is ``False``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly updated credential.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; cred = sc.credentials.edit()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># Uploading files as necessary</span>
        <span class="n">kw</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_upload_files</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;credential/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CredentialAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a credential.</span>
<span class="sd">        :sc-api:`credential: delete &lt;Credential.html#credential_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the credential to remove.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.credentials.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;credential/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CredentialAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of credential definitions.</span>
<span class="sd">        + :sc-api:`credential: list &lt;Credential.html#CredentialRESTReference-/credential&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each credential.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of credential resources.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for cred in sc.credentials.list():</span>
<span class="sd">            ...     pprint(cred)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;credential&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CredentialAPI.tags"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI.tags">[docs]</a>    <span class="k">def</span> <span class="nf">tags</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of unique tags associated to credentials.</span>
<span class="sd">        :sc-api:`credential: tags &lt;Credential.html#CredentialRESTReference-/credential/tag&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of tags</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tags = sc.credentials.tags()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;credential/tag&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CredentialAPI.share"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.credentials.CredentialAPI.share">[docs]</a>    <span class="k">def</span> <span class="nf">share</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">groups</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Shares the specified credential to another user group.</span>
<span class="sd">        :sc-api:`credential: share &lt;Credential.html#CredentialRESTReference-/credential/{id}/share&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric id for the credential.</span>
<span class="sd">            *groups (int): The numeric id of the group(s) to share to.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The updated credential resource.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.credentials.share(1, group_1, group_2)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;credential/</span><span class="si">{}</span><span class="s1">/share&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
                <span class="s1">&#39;groups&#39;</span><span class="p">:</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;group:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">groups</span><span class="p">]})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.credentials</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>