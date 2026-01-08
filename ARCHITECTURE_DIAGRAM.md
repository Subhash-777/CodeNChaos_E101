# Architecture Diagram: Dynamic Updates & User-Specific Data

## Current Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                      Dashboard Page                        │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │ Header                                               │  │  │
│  │  │ [Refresh Button] [Sync Button] [Chat Button]        │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │ WorkContexts Component                               │  │  │
│  │  │ Auto-refresh: Every 30 seconds                       │  │  │
│  │  │ Fetch: /api/contexts (with X-User-Id header)        │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │ TaskDetection Component                              │  │  │
│  │  │ Auto-refresh: Every 30 seconds                       │  │  │
│  │  │ Fetch: /api/tasks (with X-User-Id header)           │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │ RecommendedTasks Component                           │  │  │
│  │  │ Auto-refresh: Every 30 seconds                       │  │  │
│  │  │ Fetch: /api/tasks (with X-User-Id header)           │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │ PriorityExplanation Component                        │  │  │
│  │  │ Auto-refresh: Every 30 seconds                       │  │  │
│  │  │ Fetch: /api/tasks (with X-User-Id header)           │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │ WorkHabitInsights Component                          │  │  │
│  │  │ Auto-refresh: Every 30 seconds                       │  │  │
│  │  │ Fetch: /api/cognitive-load + /api/insights          │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │
         │ HTTP/HTTPS (with X-User-Id header)
         │ Cache bypass: ?t=${Date.now()}
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI/Python)                       │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ API Endpoints (require X-User-Id header)                  │  │
│  │ ├─ GET /api/contexts      → get_active_contexts()        │  │
│  │ ├─ GET /api/tasks         → get_prioritized_tasks()      │  │
│  │ ├─ GET /api/cognitive-load → get_cognitive_load()        │  │
│  │ ├─ GET /api/insights      → get_latest_insights()        │  │
│  │ ├─ GET /api/recommendations → get_recommendations()      │  │
│  │ ├─ GET /api/dashboard     → Combined dashboard data      │  │
│  │ └─ POST /api/google/sync  → Sync + toggle dataset        │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Data Services (data_loader.py)                            │  │
│  │ ├─ get_user_specific_mock_data(user_id)                  │  │
│  │ │  └─ Returns Dataset 1 or Dataset 2 based on toggle    │  │
│  │ └─ toggle_user_dataset(user_id)                          │  │
│  │    └─ Tracks: _sync_counter[user_id] = 0 or 1          │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Google Services (google_sync.py)                          │  │
│  │ └─ sync_all_google_data(user_id)                         │  │
│  │    └─ Calls toggle_user_dataset()                        │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │
         │ Read/Write user-specific data
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA STORAGE (Filesystem)                     │
│  /backend/data/                                                 │
│  ├─ user_test_a/                                               │
│  │  ├─ calendar.json       (Real Google Calendar data)          │
│  │  └─ emails.json         (Real Gmail data)                    │
│  │  └─ _sync_counter: 1    (Dataset 2: Q1 Campaign)            │
│  │                                                              │
│  ├─ user_test_b/                                               │
│  │  ├─ calendar.json       (Real Google Calendar data)          │
│  │  └─ emails.json         (Real Gmail data)                    │
│  │  └─ _sync_counter: 0    (Dataset 1: Engineering Sprint)     │
│  │                                                              │
│  └─ mock.json              (Base mock data for all users)       │
│     ├─ Dataset 1: Engineering Sprint focus                      │
│     └─ Dataset 2: Q1 Campaign focus                             │
└─────────────────────────────────────────────────────────────────┘
```

## Update Timing Sequence

```
TIME: 0s
├─ Component mounts
├─ Calls fetchTasks(userId) with X-User-Id header
├─ Backend returns user-specific tasks
└─ Component renders initial data

TIME: 30s
├─ Auto-refresh timer fires
├─ Calls fetchTasks(userId) again with cache-bypass timestamp
├─ Backend returns potentially updated user-specific tasks
└─ Component updates if data changed

TIME: 60s
├─ Auto-refresh timer fires again
├─ Calls fetchTasks(userId) with new timestamp
├─ Backend returns current user-specific tasks
└─ Component updates if data changed

TIME: User clicks "Sync" button
├─ POST /api/google/sync with X-User-Id
├─ Backend:
│  ├─ Syncs with Google Calendar & Gmail
│  └─ Calls toggle_user_dataset() → Changes dataset for this user
├─ Frontend calls triggerRefresh() at 500ms
├─ All components detect refreshKey change
├─ All components immediately fetch fresh data
├─ Frontend calls triggerRefresh() again at 1500ms
└─ Second refresh ensures data consistency

TIME: 90s
├─ Auto-refresh continues every 30s
└─ Shows new data if sync changed it
```

## User Data Isolation

```
REQUEST from User A:
┌──────────────────────────────────────────────┐
│ GET /api/contexts                            │
│ Headers: X-User-Id: user_test_a              │
└──────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────┐
│ Backend validates header                     │
│ Checks: /backend/data/user_test_a/           │
│ Uses: _sync_counter[user_test_a] = 1        │
│ Returns: Dataset 2 data                      │
│ "Q1 Campaign" context                        │
└──────────────────────────────────────────────┘

REQUEST from User B:
┌──────────────────────────────────────────────┐
│ GET /api/contexts                            │
│ Headers: X-User-Id: user_test_b              │
└──────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────┐
│ Backend validates header                     │
│ Checks: /backend/data/user_test_b/           │
│ Uses: _sync_counter[user_test_b] = 0        │
│ Returns: Dataset 1 data                      │
│ "Engineering Sprint" context                 │
└──────────────────────────────────────────────┘
```

## Component Lifecycle with Auto-Refresh

```
┌─────────────────────────────────────────────────────────┐
│ Component Lifecycle                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 1. Component Mounts                                     │
│    └─ useEffect(() => { ... }, [userId, refreshKey])   │
│                                                          │
│ 2. Initial Load                                         │
│    ├─ Check userId exists                              │
│    └─ Call loadContexts()                              │
│       └─ Fetch data from API                           │
│       └─ Update state: setContexts(data)               │
│                                                          │
│ 3. Start Auto-Refresh Timer                            │
│    ├─ setInterval(() => {                              │
│    │   loadContexts()  // Re-fetch every 30 seconds     │
│    │ }, 30000)                                          │
│    └─ Save intervalId                                  │
│                                                          │
│ 4. Component Updates (Every 30 seconds)                │
│    ├─ Timer fires                                       │
│    ├─ Call loadContexts()                              │
│    ├─ Fetch fresh data                                 │
│    └─ Update state if changed                          │
│                                                          │
│ 5. Manual Refresh Trigger                              │
│    ├─ User clicks "Refresh" or "Sync"                  │
│    ├─ SyncContext.triggerRefresh() called              │
│    ├─ refreshKey incremented                           │
│    ├─ Component detects dependency change              │
│    └─ Immediately calls loadContexts()                 │
│                                                          │
│ 6. Component Unmounts                                  │
│    ├─ Return cleanup function                          │
│    ├─ clearInterval(autoRefreshInterval)               │
│    └─ Prevents memory leaks                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Key Improvements

```
BEFORE:
├─ Static data on load
├─ No automatic updates
├─ Had to manually click sync
├─ Same data for all users
└─ No cache bypass

AFTER:
├─ Dynamic data every 30s ✅
├─ Automatic updates ✅
├─ Manual refresh button ✅
├─ Different data per user ✅
├─ Cache bypass enabled ✅
├─ Sync triggers refresh ✅
└─ Dataset toggle on sync ✅
```

---

## Summary

The dashboard now:
1. **Updates automatically** every 30 seconds
2. **Shows different data** for different users
3. **Provides manual refresh** for immediate updates
4. **Toggles datasets** on sync for variety
5. **Maintains user isolation** at backend level
6. **Bypasses caching** for fresh data
7. **Properly cleans up** intervals to prevent memory leaks
