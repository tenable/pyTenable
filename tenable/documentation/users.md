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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.users</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.users</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Users</span>
<span class="sd">=====</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`User &lt;User.html&gt;` API.  These items are typically seen under the</span>
<span class="sd">**Users** section of Tenable.sc.</span>
<span class="sd">Methods available on ``sc.users``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: UserAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<div class="viewcode-block" id="UserAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.users.UserAPI">[docs]</a><span class="k">class</span> <span class="nc">UserAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a user definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;role&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate role as int and pass to roleID</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;roleID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;role&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;role&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;role&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;group&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate group asd int and pass to groupID</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;groupID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;group&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;group&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;group&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;org&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate org as int and pass to orgID</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;orgID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;org&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;org&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;responsibility&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate responsibility as an int and pass to responsibleAssetID</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;responsibleAssetID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;responsibility&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;responsibility&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;responsibility&#39;</span><span class="p">])</span>
        <span class="c1"># all of the following keys are string values and do not require any</span>
        <span class="c1"># case conversion.  We will simply iterate through them and verify that</span>
        <span class="c1"># they are in-fact strings.</span>
        <span class="n">keys</span> <span class="o">=</span> <span class="p">[</span>
            <span class="s1">&#39;ldapUsername&#39;</span><span class="p">,</span> <span class="s1">&#39;username&#39;</span><span class="p">,</span> <span class="s1">&#39;firstname&#39;</span><span class="p">,</span> <span class="s1">&#39;lastname&#39;</span><span class="p">,</span> <span class="s1">&#39;title&#39;</span><span class="p">,</span>
            <span class="s1">&#39;email&#39;</span><span class="p">,</span> <span class="s1">&#39;address&#39;</span><span class="p">,</span> <span class="s1">&#39;city&#39;</span><span class="p">,</span> <span class="s1">&#39;state&#39;</span><span class="p">,</span> <span class="s1">&#39;country&#39;</span><span class="p">,</span> <span class="s1">&#39;phone&#39;</span><span class="p">,</span> <span class="s1">&#39;fax&#39;</span><span class="p">,</span>
            <span class="s1">&#39;fingerprint&#39;</span><span class="p">,</span> <span class="s1">&#39;status&#39;</span>
        <span class="p">]</span>
        <span class="k">for</span> <span class="n">k</span> <span class="ow">in</span> <span class="n">keys</span><span class="p">:</span>
            <span class="k">if</span> <span class="n">k</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="n">k</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="n">k</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;is_locked&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the is_locked keyword from a boolean value into a string</span>
            <span class="c1"># interpretation of that value.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;locked&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;is_locked&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;is_locked&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;is_locked&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;auth_type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify that auth_type is one of the correct possible values and</span>
            <span class="c1"># store it within the camelCased version of the parameter.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;authType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;auth_type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;ldap&#39;</span><span class="p">,</span> <span class="s1">&#39;legacy&#39;</span><span class="p">,</span> <span class="s1">&#39;saml&#39;</span><span class="p">,</span> <span class="s1">&#39;tns&#39;</span><span class="p">,</span> <span class="s1">&#39;linked&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;email_notice&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Verify that email_notice is one of the correct possible values and</span>
            <span class="c1"># store it within the camelCased version of the parameter.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;emailNotice&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;email_notice&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;email_notice&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                    <span class="s1">&#39;both&#39;</span><span class="p">,</span> <span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="s1">&#39;none&#39;</span><span class="p">,</span> <span class="s1">&#39;password&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;email_notice&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;timezone&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the timezone parameter into the preference dictionary</span>
            <span class="c1"># item that&#39;s expected by the API.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span>
                <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="s1">&#39;timezone&#39;</span><span class="p">,</span>
                <span class="s1">&#39;tag&#39;</span><span class="p">:</span> <span class="s1">&#39;system&#39;</span><span class="p">,</span>
                <span class="s1">&#39;value&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;timezone&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;timezone&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="p">}]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;timezone&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;update_password&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the update_password keyword from a boolean value into a</span>
            <span class="c1"># string interpretation of that value.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;mustChangePassword&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;update_password&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;update_password&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;update_password&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;managed_usergroups&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the managed_groups list into a listing of dictionaries</span>
            <span class="c1"># with an id parameter.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managedUsersGroups&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;group:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                    <span class="s1">&#39;managed_usergroups&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managed_usergroups&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managed_usergroups&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;managed_userobjs&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the managed_groups list into a listing of dictionaries</span>
            <span class="c1"># with an id parameter.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managedObjectsGroups&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;group:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                    <span class="s1">&#39;managed_userobjs&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managed_userobjs&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managed_userobjs&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;default_reports&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Should the default user reports be built as part of the user</span>
            <span class="c1"># creation?</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;importReports&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;default_reports&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;default_reports&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;default_reports&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;default_dashboards&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Should the default user dashboards be built as part of the user</span>
            <span class="c1"># creation?</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;importDashboards&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;default_dashboards&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;default_dashboards&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;default_dashboards&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;default_reportcards&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Should the default user dashboards be built as part of the user</span>
            <span class="c1"># creation?</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;importARCs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;default_reportcards&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;default_reportcards&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;default_reportcards&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;ldap_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the ldap_id attribute to a subdocument of &quot;ldap&quot;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ldap&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ldap_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ldap_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ldap_id&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="UserAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.users.UserAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="n">role</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a user.</span>
<span class="sd">        :sc-api:`user: create &lt;User.html#user_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            username (str):</span>
<span class="sd">                The username for the account</span>
<span class="sd">            password (str):</span>
<span class="sd">                The password for the user to create</span>
<span class="sd">            role (int):</span>
<span class="sd">                The role that should be assigned to this user.</span>
<span class="sd">            address (str, optional):</span>
<span class="sd">                Optional street address information to associate to the user.</span>
<span class="sd">            auth_type (str, optional):</span>
<span class="sd">                The Authentication type to use for the user.  Valid options are</span>
<span class="sd">                ``ldap``, ``legacy``, ``saml``, and ``tns``.  If left unspecified</span>
<span class="sd">                the default is ``tns``.</span>
<span class="sd">            city (str, optional):</span>
<span class="sd">                Optional city information to associate to the user.</span>
<span class="sd">            country (str, optional):</span>
<span class="sd">                Optional country information to associate to the user.</span>
<span class="sd">            default_dashboards (bool, optional):</span>
<span class="sd">                Should the default dashboards be created for the user?  If left</span>
<span class="sd">                unspecified, the default is True.</span>
<span class="sd">            default_reportcards (bool, optional):</span>
<span class="sd">                Should the default report cards be created for the user?  If</span>
<span class="sd">                left unspecified, the default is True.</span>
<span class="sd">            default_reports (bool, optional):</span>
<span class="sd">                Should the default reports be created for the user?  If left</span>
<span class="sd">                unspecified, the default is True.</span>
<span class="sd">            email (str, optional):</span>
<span class="sd">                The email address to associate to the user.</span>
<span class="sd">            email_notice (str, optional):</span>
<span class="sd">                What type of events should generate an email notification?</span>
<span class="sd">                Valid types are ``id``, ``password``, ``both``, ``none``.</span>
<span class="sd">            fax (str, optional):</span>
<span class="sd">                A fax number to associate to the user.</span>
<span class="sd">            fingerprint (str, optional):</span>
<span class="sd">                A fingerprint to associate to the user.</span>
<span class="sd">            firstname (str, optional):</span>
<span class="sd">                A first name to associate to the user.</span>
<span class="sd">            group (int, optional):</span>
<span class="sd">                A group to associate to the user.  This parameter is required</span>
<span class="sd">                for users that are not Administrators.</span>
<span class="sd">            is_locked (bool, optional):</span>
<span class="sd">                If the account locked?  If left unspecified the default is False.</span>
<span class="sd">            ldap_id (int, optional):</span>
<span class="sd">                If specifying an LDAP auth type, this is the numeric identifier</span>
<span class="sd">                for the LDAP configuration to use.</span>
<span class="sd">            managed_usergroups (list, optional):</span>
<span class="sd">                A list of group ids that the user is allowed to manage users</span>
<span class="sd">                within.</span>
<span class="sd">            managed_userobjs (list, optional):</span>
<span class="sd">                A list of group ids that the user is allowed to manage objects</span>
<span class="sd">                within.  This includes asset lists, reports, etc.</span>
<span class="sd">            org (int, optional):</span>
<span class="sd">                If logged in as an administrator, and creating a security</span>
<span class="sd">                manager account, the organization id must be passed in order to</span>
<span class="sd">                inform Tenable.sc which organization to create the security</span>
<span class="sd">                manager within.</span>
<span class="sd">            phone (str, optional):</span>
<span class="sd">                A phone number to associate to the user.</span>
<span class="sd">            responsibility (int, optional):</span>
<span class="sd">                The asset list detailing what assets the user is responsible</span>
<span class="sd">                for.  A value of ``0`` denotes all assets, any other non-zero</span>
<span class="sd">                integer must be the id of the asset list to associate to the</span>
<span class="sd">                user.</span>
<span class="sd">            state (str, optional):</span>
<span class="sd">                The state to associate to the user.</span>
<span class="sd">            timezone (str, optional):</span>
<span class="sd">                A timezone other than the system timezone to associate to the</span>
<span class="sd">                user.  This will impact all times displayed within the user</span>
<span class="sd">                interface.</span>
<span class="sd">            title (str, optional):</span>
<span class="sd">                A title to associate to the user.</span>
<span class="sd">            update_password (bool, optional):</span>
<span class="sd">                Should the user be forced to update their password next login?</span>
<span class="sd">                If left unspecified, the default is False.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created user.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; user = sc.users.create(&#39;username&#39;, &#39;password&#39;, 1, group=1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;username&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">username</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;password&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">password</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;role&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">role</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auth_type&#39;</span><span class="p">,</span> <span class="s1">&#39;tns&#39;</span><span class="p">)</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;responsibleAssetID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;user&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="UserAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.users.UserAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific user.</span>
<span class="sd">        :sc-api:`user: details &lt;User.html#UserRESTReference-/user/{id}&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the user.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The user resource record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; user = sc.users.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(user)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;user/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="UserAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.users.UserAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits a user.</span>
<span class="sd">        :sc-api:`user: edit &lt;User.html#user_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            address (str, optional):</span>
<span class="sd">                Optional street address information to associate to the user.</span>
<span class="sd">            auth_type (str, optional):</span>
<span class="sd">                The Authentication type to use for the user.  Valid options are</span>
<span class="sd">                ``ldap``, ``legacy``, ``saml``, and ``tns``.  If left unspecified</span>
<span class="sd">                the default is ``tns``.</span>
<span class="sd">            city (str, optional):</span>
<span class="sd">                Optional city information to associate to the user.</span>
<span class="sd">            country (str, optional):</span>
<span class="sd">                Optional country information to associate to the user.</span>
<span class="sd">            default_dashboards (bool, optional):</span>
<span class="sd">                Should the default dashboards be created for the user?  If left</span>
<span class="sd">                unspecified, the default is True.</span>
<span class="sd">            default_reportcards (bool, optional):</span>
<span class="sd">                Should the default report cards be created for the user?  If</span>
<span class="sd">                left unspecified, the default is True.</span>
<span class="sd">            default_reports (bool, optional):</span>
<span class="sd">                Should the default reports be created for the user?  If left</span>
<span class="sd">                unspecified, the default is True.</span>
<span class="sd">            email (str, optional):</span>
<span class="sd">                The email address to associate to the user.</span>
<span class="sd">            email_notice (str, optional):</span>
<span class="sd">                What type of events should generate an email notification?</span>
<span class="sd">                Valid types are ``id``, ``password``, ``both``, ``none``.</span>
<span class="sd">            fax (str, optional):</span>
<span class="sd">                A fax number to associate to the user.</span>
<span class="sd">            fingerprint (str, optional):</span>
<span class="sd">                A fingerprint to associate to the user.</span>
<span class="sd">            firstname (str, optional):</span>
<span class="sd">                A first name to associate to the user.</span>
<span class="sd">            group (int, optional):</span>
<span class="sd">                A group to associate to the user.  This parameter is required</span>
<span class="sd">                for users that are not Administrators.</span>
<span class="sd">            is_locked (bool, optional):</span>
<span class="sd">                If the account locked?  If left unspecified the default is False.</span>
<span class="sd">            ldap_id (int, optional):</span>
<span class="sd">                If specifying an LDAP auth type, this is the numeric identifier</span>
<span class="sd">                for the LDAP configuration to use.</span>
<span class="sd">            managed_usergroups (list, optional):</span>
<span class="sd">                A list of group ids that the user is allowed to manage users</span>
<span class="sd">                within.</span>
<span class="sd">            managed_userobjs (list, optional):</span>
<span class="sd">                A list of group ids that the user is allowed to manage objects</span>
<span class="sd">                within.  This includes asset lists, reports, etc.</span>
<span class="sd">            org (int, optional):</span>
<span class="sd">                If logged in as an administrator, and creating a security</span>
<span class="sd">                manager account, the organization id must be passed in order to</span>
<span class="sd">                inform Tenable.sc which organization to create the security</span>
<span class="sd">                manager within.</span>
<span class="sd">            password (str, optional):</span>
<span class="sd">                The user password</span>
<span class="sd">            phone (str, optional):</span>
<span class="sd">                A phone number to associate to the user.</span>
<span class="sd">            responsibility (int, optional):</span>
<span class="sd">                The asset list detailing what assets the user is responsible</span>
<span class="sd">                for.  A value of ``0`` denotes all assets, any other non-zero</span>
<span class="sd">                integer must be the id of the asset list to associate to the</span>
<span class="sd">                user.</span>
<span class="sd">            role (int, optional):</span>
<span class="sd">                The role that should be assigned to this user.</span>
<span class="sd">            state (str, optional):</span>
<span class="sd">                The state to associate to the user.</span>
<span class="sd">            timezone (str, optional):</span>
<span class="sd">                A timezone other than the system timezone to associate to the</span>
<span class="sd">                user.  This will impact all times displayed within the user</span>
<span class="sd">                interface.</span>
<span class="sd">            title (str, optional):</span>
<span class="sd">                A title to associate to the user.</span>
<span class="sd">            update_password (bool, optional):</span>
<span class="sd">                Should the user be forced to update their password next login?</span>
<span class="sd">                If left unspecified, the default is False.</span>
<span class="sd">            username (str, optional):</span>
<span class="sd">                The username for the account</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly updated user.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; user = sc.users.edit(1, username=&#39;newusername&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;user/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="UserAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.users.UserAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a user.</span>
<span class="sd">        :sc-api:`user: delete &lt;User.html#user_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the user to remove.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.users.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;user/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="UserAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.users.UserAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of user definitions.</span>
<span class="sd">        :sc-api:`user: list &lt;User.html#user_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each user.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of user resources.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for user in sc.users.list():</span>
<span class="sd">            ...     pprint(user)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;user&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.users</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>