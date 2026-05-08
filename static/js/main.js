/* Construction Focus Journal A.B.U Zaria — Main JS */

document.addEventListener('DOMContentLoaded', function () {

  // ── Sidebar Mobile Toggle ──────────────────────────────
  const toggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');

  if (toggle && sidebar) {
    toggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', function (e) {
      if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // ── Auto-generate slug from title ─────────────────────
  const titleInput = document.getElementById('id_title');
  const slugInput  = document.getElementById('id_slug');

  if (titleInput && slugInput) {
    titleInput.addEventListener('input', function () {
      if (slugInput.dataset.userEdited) return;
      slugInput.value = titleInput.value
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_]+/g, '-')
        .replace(/^-+|-+$/g, '');
    });

    slugInput.addEventListener('input', function () {
      slugInput.dataset.userEdited = 'true';
    });
  }

  // ── Auto-dismiss alerts ────────────────────────────────
  const alerts = document.querySelectorAll('.alert.alert-success, .alert.alert-info');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 4500);
  });

  // ── Navbar scroll effect ───────────────────────────────
  const mainNav = document.getElementById('mainNav');
  if (mainNav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 60) {
        mainNav.style.padding = '0.6rem 0';
      } else {
        mainNav.style.padding = '0.9rem 0';
      }
    });
  }

  // ── Issue filter by volume (article form) ─────────────
  const volumeSelect = document.getElementById('id_volume');
  const issueSelect  = document.getElementById('id_issue');

  if (volumeSelect && issueSelect) {
    volumeSelect.addEventListener('change', function () {
      const volumeId = this.value;
      const currentIssue = issueSelect.value;

      Array.from(issueSelect.options).forEach(function (opt) {
        if (opt.value === '') return;
        const optVolume = opt.dataset.volume;
        if (optVolume && volumeId && optVolume !== volumeId) {
          opt.style.display = 'none';
          if (opt.value === currentIssue) issueSelect.value = '';
        } else {
          opt.style.display = '';
        }
      });
    });
  }

});
