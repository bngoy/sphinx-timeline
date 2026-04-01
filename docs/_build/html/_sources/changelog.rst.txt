Changelog
=========

.. timeline::
   :status: development

   .. timeline-item::
      :tags: need for speed

      **Project Theseus: removing BuildKit**

      The largest engine change since the project began. Replacing BuildKit
      with a native solver, unlocking robust remote caching, cache
      observability, and more flexible module execution.

   .. timeline-item::
      :tags: cloud

      **Cloud Engines**

      Fully managed engines with auto-scaling and distributed caching.
      Run ``dagger --cloud`` and your pipelines execute in the cloud —
      with your local context preserved seamlessly. In early access.

   .. timeline-item::

      **Modules v2**

      A major upgrade to how modules interact with your project. Modules
      get a typed API to your workspace, replacing rigid sandbox constraints
      with dynamic context — less complexity for developers, more control
      for platform engineers.

.. timeline::
   :version: v0.20.2
   :date: Mar 19, 2026
   :status: released

   .. timeline-item::
      :tags: need for speed

      **Dang: a native language**

      A scripting language designed specifically for the engine, now with a
      native runtime built in. Loads types directly from the engine at
      runtime — no codegen, near-instant startup, and concise syntax.

   .. timeline-item::

      **New terminal UI**

      A ground-up rebuild of the interactive TUI. Output uses your
      terminal's native scrollback — scroll freely, click links, select
      text — no more fixed viewport. Also adds inline search with ``/``.

   .. timeline-item::

      **Vault OIDC authentication**

      The Vault secret provider now supports OIDC login. If no token or
      environment credentials are set, your browser opens for OIDC
      authentication and caches the token with automatic expiry.

   .. timeline-item::
      :tags: cloud, performance

      **Suppress update notifications in CI**

      Set ``DAGGER_NO_UPDATE_CHECK=1`` to skip the CLI version check
      entirely — no network request, no stderr noise. Useful in CI
      environments where CLI versions are pinned.

.. timeline::
   :version: v0.19.0
   :date: Feb 10, 2026
   :status: released

   .. timeline-item::
      :tags: security

      **New secrets provider: GCP Secret Manager**

      Google Cloud Secret Manager is now a native secret provider. Use
      ``gcp://secret-name`` with Application Default Credentials, service
      account keys, or Workload Identity on GKE.

   .. timeline-item::

      **Stability fixes**

      Running inside a container with a mounted git worktree no longer
      crashes. Module dependencies pinned by branch or tag name instead of
      commit SHA now resolve correctly.
