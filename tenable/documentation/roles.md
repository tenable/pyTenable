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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.roles</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.roles</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Roles</span>
<span class="sd">=====</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Roles &lt;Role.html&gt;` API.  These items are typically seen under the</span>
<span class="sd">**User Roles** section of Tenable.sc.</span>
<span class="sd">Methods available on ``sc.roles``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: RoleAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<div class="viewcode-block" id="RoleAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.roles.RoleAPI">[docs]</a><span class="k">class</span> <span class="nc">RoleAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a role definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the name parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the description parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;permScan&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;can_scan&#39;</span><span class="p">,</span>
                                     <span class="n">kw</span><span class="o">.</span><span class="n">pop</span><span class="p">(</span><span class="s1">&#39;can_scan&#39;</span><span class="p">,</span> <span class="kc">None</span><span class="p">),</span>
                                     <span class="nb">str</span><span class="p">,</span>
                                     <span class="n">case</span><span class="o">=</span><span class="s1">&#39;lower&#39;</span><span class="p">,</span>
                                     <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;full&#39;</span><span class="p">,</span> <span class="s1">&#39;policy&#39;</span><span class="p">,</span> <span class="s1">&#39;none&#39;</span><span class="p">],</span>
                                     <span class="n">default</span><span class="o">=</span><span class="s1">&#39;none&#39;</span><span class="p">)</span>
        <span class="c1"># Snake-cased boolean role mapping to the API attributes.</span>
        <span class="n">mapping</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;manage_groups&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageGroups&#39;</span><span class="p">,</span>
            <span class="s1">&#39;manage_roles&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageRoles&#39;</span><span class="p">,</span>
            <span class="s1">&#39;manage_images&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageImages&#39;</span><span class="p">,</span>
            <span class="s1">&#39;manage_relationships&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageGroupRelationships&#39;</span><span class="p">,</span>
            <span class="s1">&#39;manage_blackout_windows&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageBlackoutWindows&#39;</span><span class="p">,</span>
            <span class="s1">&#39;manage_attributes&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageAttributeSets&#39;</span><span class="p">,</span>
            <span class="s1">&#39;create_tickets&#39;</span><span class="p">:</span> <span class="s1">&#39;permCreateTickets&#39;</span><span class="p">,</span>
            <span class="s1">&#39;create_alerts&#39;</span><span class="p">:</span> <span class="s1">&#39;permCreateAlerts&#39;</span><span class="p">,</span>
            <span class="s1">&#39;create_auditfiles&#39;</span><span class="p">:</span> <span class="s1">&#39;permCreateAuditFiles&#39;</span><span class="p">,</span>
            <span class="s1">&#39;create_ldap_assets&#39;</span><span class="p">:</span> <span class="s1">&#39;permCreateLDAPAssets&#39;</span><span class="p">,</span>
            <span class="s1">&#39;create_policies&#39;</span><span class="p">:</span> <span class="s1">&#39;permCreatePolicies&#39;</span><span class="p">,</span>
            <span class="s1">&#39;purge_tickets&#39;</span><span class="p">:</span> <span class="s1">&#39;permPurgeTickets&#39;</span><span class="p">,</span>
            <span class="s1">&#39;purge_scans&#39;</span><span class="p">:</span> <span class="s1">&#39;permPurgeScanResults&#39;</span><span class="p">,</span>
            <span class="s1">&#39;purge_reports&#39;</span><span class="p">:</span> <span class="s1">&#39;permPurgeReportResults&#39;</span><span class="p">,</span>
            <span class="s1">&#39;can_agent_scan&#39;</span><span class="p">:</span> <span class="s1">&#39;permAgentsScan&#39;</span><span class="p">,</span>
            <span class="s1">&#39;can_share&#39;</span><span class="p">:</span> <span class="s1">&#39;permShareObjects&#39;</span><span class="p">,</span>
            <span class="s1">&#39;can_feed_update&#39;</span><span class="p">:</span> <span class="s1">&#39;permUpdateFeeds&#39;</span><span class="p">,</span>
            <span class="s1">&#39;can_import_scan&#39;</span><span class="p">:</span> <span class="s1">&#39;permUploadNessusResults&#39;</span><span class="p">,</span>
            <span class="s1">&#39;can_view_logs&#39;</span><span class="p">:</span> <span class="s1">&#39;permViewOrgLogs&#39;</span><span class="p">,</span>
            <span class="s1">&#39;manage_accepted_risk_rules&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageAcceptRiskRules&#39;</span><span class="p">,</span>
            <span class="s1">&#39;manage_recast_risk_rules&#39;</span><span class="p">:</span> <span class="s1">&#39;permManageRecastRiskRules&#39;</span><span class="p">,</span>
        <span class="p">}</span>
        <span class="c1"># iterate through the keys, converting the boolean values to the</span>
        <span class="c1"># lowercased strings values that the API expects to see.</span>
        <span class="k">for</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">mapping</span><span class="o">.</span><span class="n">keys</span><span class="p">():</span>
            <span class="k">if</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="n">mapping</span><span class="p">[</span><span class="n">key</span><span class="p">]]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="n">key</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="n">key</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
                <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="n">key</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="RoleAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.roles.RoleAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a role.</span>
<span class="sd">        :sc-api:`role: create &lt;Role.html#role_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            name (str): The name of the new role to create.</span>
<span class="sd">            descrioption (str, optional):</span>
<span class="sd">                A description for the role to be created.</span>
<span class="sd">            can_agent_scan (bool, optional):</span>
<span class="sd">                Are members of this role allowed to perform agent scans? If left</span>
<span class="sd">                unspecified the default is ``False``.</span>
<span class="sd">            can_feed_update (bool, optional):</span>
<span class="sd">                Are members of this role allowed to perform feed updates? If</span>
<span class="sd">                left unspecified, the default is ``False``.</span>
<span class="sd">            can_import_scan (bool, optional):</span>
<span class="sd">                Are members of this role allowed to import scans?  If left</span>
<span class="sd">                unspecified, the default is ``False``.</span>
<span class="sd">            can_scan (str, optional):</span>
<span class="sd">                Are members of this role allowed to perform scans?  Accepted</span>
<span class="sd">                values are `full`, `policy`, and `none`.  If left unspecified,</span>
<span class="sd">                the default is `none`.</span>
<span class="sd">            can_share (bool, optional):</span>
<span class="sd">                Are members of this role allowed to share objects with other</span>
<span class="sd">                groups?  If left unspecified, the default is ``False``.</span>
<span class="sd">            can_view_logs (bool, optional):</span>
<span class="sd">                Are members of this role allowed to view the organizational</span>
<span class="sd">                logs from Tenable.sc?  If left unspecified, the default is</span>
<span class="sd">                ``False``.</span>
<span class="sd">            create_alerts (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create alerts? If left</span>
<span class="sd">                unspecified, the default is ``False``.</span>
<span class="sd">            create_auditfiles (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create their own audit</span>
<span class="sd">                files?  If left unspecified, the default is ``False``.</span>
<span class="sd">            create_ldap_assets (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create LDAP Query Asset</span>
<span class="sd">                Lists?  If left unspecified, the default is ``False``.</span>
<span class="sd">            create_policies (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create scan policies?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            create_tickets (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create tickets?  If left</span>
<span class="sd">                unspecified, the default is ``False``.</span>
<span class="sd">            manage_accepted_risk_rules (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage accepted risk rules?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_attributes (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage attribute sets?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_blackout_windows (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage scanning blackout</span>
<span class="sd">                windows?  If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_groups (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage user groups?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_images (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage report images?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_recast_risk_rules (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage recast risk rules?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_relationships (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage the user group</span>
<span class="sd">                relationships?  If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_roles (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage group role</span>
<span class="sd">                configurations?  If left unspecified, the default is ``False``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created role.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; role = sc.roles.create(&#39;Example Role&#39;,</span>
<span class="sd">            ...     can_scan=True, can_import_scan=True)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;role&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RoleAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.roles.RoleAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific role.</span>
<span class="sd">        :sc-api:`role: details &lt;Role.html#role_id_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the role.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The role resource record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; role = sc.roles.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(role)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;role/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RoleAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.roles.RoleAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits a role.</span>
<span class="sd">        :sc-api:`role: edit &lt;Role.html#role_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the role.</span>
<span class="sd">            name (str, optional):</span>
<span class="sd">                The name of the new role to create.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                A description for the role to be created.</span>
<span class="sd">            can_agent_scan (bool, optional):</span>
<span class="sd">                Are members of this role allowed to perform agent scans? If left</span>
<span class="sd">                unspecified the default is ``False``.</span>
<span class="sd">            can_feed_update (bool, optional):</span>
<span class="sd">                Are members of this role allowed to perform feed updates? If</span>
<span class="sd">                left unspecified, the default is ``False``.</span>
<span class="sd">            can_import_scan (bool, optional):</span>
<span class="sd">                Are members of this role allowed to import scans?  If left</span>
<span class="sd">                unspecified, the default is ``False``.</span>
<span class="sd">            can_scan (bool, optional):</span>
<span class="sd">                Are members of this role allowed to perform scans?  If left</span>
<span class="sd">                unspecified, the default is ``False``.</span>
<span class="sd">            can_share (bool, optional):</span>
<span class="sd">                Are members of this role allowed to share objects with other</span>
<span class="sd">                groups?  If left unspecified, the default is ``False``.</span>
<span class="sd">            can_view_logs (bool, optional):</span>
<span class="sd">                Are members of this role allowed to view the organizational</span>
<span class="sd">                logs from Tenable.sc?  If left unspecified, the default is</span>
<span class="sd">                ``False``.</span>
<span class="sd">            create_alerts (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create alerts? If left</span>
<span class="sd">                unspecified, the default is ``False``.</span>
<span class="sd">            create_auditfiles (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create their own audit</span>
<span class="sd">                files?  If left unspecified, the default is ``False``.</span>
<span class="sd">            create_ldap_assets (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create LDAP Query Asset</span>
<span class="sd">                Lists?  If left unspecified, the default is ``False``.</span>
<span class="sd">            create_policies (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create scan policies?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            create_tickets (bool, optional):</span>
<span class="sd">                Are members of this role allowed to create tickets?  If left</span>
<span class="sd">                unspecified, the default is ``False``.</span>
<span class="sd">            manage_accepted_risk_rules (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage accepted risk rules?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_attributes (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage attribute sets?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_blackout_windows (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage scanning blackout</span>
<span class="sd">                windows?  If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_groups (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage user groups?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_images (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage report images?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_recast_risk_rules (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage recast risk rules?</span>
<span class="sd">                If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_relationships (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage the user group</span>
<span class="sd">                relationships?  If left unspecified, the default is ``False``.</span>
<span class="sd">            manage_roles (bool, optional):</span>
<span class="sd">                Are members of this role allowed to manage group role</span>
<span class="sd">                configurations?  If left unspecified, the default is ``False``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly updated role.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; role = sc.roles.create()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;role/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RoleAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.roles.RoleAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a role.</span>
<span class="sd">        :sc-api:`role: delete &lt;Role.html#role_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the role to remove.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.roles.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;role/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RoleAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.roles.RoleAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of role definitions.</span>
<span class="sd">        :sc-api:`role: list &lt;Role.html#role_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each role.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of role resources.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for role in sc.roles.list():</span>
<span class="sd">            ...     pprint(role)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;role&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.roles</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>